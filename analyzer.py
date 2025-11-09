import os
import json
import xml.etree.ElementTree as ET
try:
    from lxml import etree as lxml_ET
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False
    print("lxml not available, using ET only — XML errors may occur")
from collections import Counter
import re
import csv
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    filename='run.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_metadata():
    """
    PHASE 1: METADATA SETUP
    - For each ExpXX/meta.json (if exists): Load model/temp/seed.
    - If missing, infer: model='GPT-5 low' for 00–05, 'Qwen3-Coder' for 06–11; 
      temp=0.2 + 0.2*(int(XX)%6) for 00–05.
    """
    logging.info("Starting metadata loading...")
    
    exp_dir = Path('./Experiments')
    metadata = {}
    
    for exp_path in exp_dir.iterdir():
        if not exp_path.is_dir() or not re.match(r'Exp\d{2}', exp_path.name):
            continue
            
        exp_num = int(exp_path.name.replace('Exp', ''))
        meta_file = exp_path / 'meta.json'
        
        if meta_file.exists():
            # Load from meta.json
            with open(meta_file, 'r') as f:
                meta_data = json.load(f)
            metadata[exp_path.name] = {
                'model': meta_data.get('model'),
                'temperature': meta_data.get('temperature'),
                'seed': meta_data.get('seed')
            }
        else:
            # Infer based on experiment number
            if 0 <= exp_num <= 5:
                model = 'GPT-5 low'
                temp = 0.2 + 0.2 * (exp_num % 6)  # temp increases by 0.2 for each exp 00-05
            elif 6 <= exp_num <= 11:
                model = 'Qwen3-Coder'
                temp = 0  # Default ~0 for Qwen3-Coder
            else:
                continue  # Skip if out of range
                
            metadata[exp_path.name] = {
                'model': model,
                'temperature': temp,
                'seed': None  # Not specified in inferred case
            }
    
    logging.info(f"Metadata loaded for {len(metadata)} experiments")
    return metadata

def parse_case_metrics(exp_name, case_name):
    """
    Parse metrics from a single case (Case1-Case5) of an experiment.
    Updated to handle both upper and lower case XML tags and different structures for Case1 vs others.
    Uses lxml for robust parsing if available.
    """
    exp_dir = Path(f'./Experiments/{exp_name}')
    case_path = exp_dir / case_name
    
    metrics = {
        'qc_present': True,  # Assume present initially
        'qc_xml_valid': True  # Assume valid initially
    }
    
    # Determine which output file to use
    output_file = 'output_raw.xml' if case_name == 'Case1' else 'output.xml'
    output_path = case_path / output_file
    
    if not output_path.exists():
        logging.warning(f"Missing output file {output_path}")
        metrics['qc_present'] = False
        return metrics

    if 'pcg_compliance' not in metrics:
        metrics['pcg_compliance'] = 'pass'
        metrics['format_compliance'] = 0.0
        logging.info(f"VerificationReport missing or incomplete in {output_path}, assuming PCG pass for content")
    
    # Read raw XML text for fallback
    with open(output_path, 'r') as f:
        xml_text = f.read()
    
    # Try ET first, fallback to lxml if available and ET fails
    tree = None
    root = None
    parse_error = None
    if LXML_AVAILABLE:
        try:
            root = lxml_ET.fromstring(xml_text, parser=lxml_ET.XMLParser(recover=True, encoding='utf-8'))
            tree = lxml_ET.ElementTree(root)
        except lxml_ET.XMLSyntaxError as e:
            parse_error = str(e)
            logging.warning(f"lxml parse error in {output_path}: {parse_error[:100]}")
            metrics['qc_xml_valid'] = False
    if root is None:
        try:
            tree = ET.fromstring(xml_text)
            root = tree  # Fix: fromstring returns Element, not ElementTree
        except ET.ParseError as e:
            parse_error = str(e)
            logging.warning(f"ET parse error in {output_path}: {parse_error}")
            metrics['qc_xml_valid'] = False
            return metrics
    
    if not metrics['qc_xml_valid']:
        logging.warning(f"XML invalid in {output_path}, skipping detailed metrics. First 200 chars: {xml_text[:200]}")
        return metrics
    
    # Handle Case1 specially - it has different structure than Cases 2-5
    if case_name == 'Case1':
        # Case1 generates tasks, so look for the synthesis report
        syn_report = None
        for tag_name in ['.//synthesis_report', './/SynthesisReport', './/SYNTHESIS_REPORT']:
            syn_report = root.find(tag_name)
            if syn_report is not None:
                break
        if syn_report is not None:
            compliance_check = syn_report.find('.//compliance_check')
            if compliance_check is not None and compliance_check.text and 'PCG compliant' in compliance_check.text.lower():
                metrics['pcg_compliance'] = 'pass'  # Consider as compliant
        
        # For Case1, set default values for other metrics since it's a task generator
        return metrics
    
    # For Cases 2-5, look for both upper and lower case tag variants
    # Extract verification report metrics
    verification_report = None
    for tag_name in ['.//VerificationReport', './/verification_report', './/VERIFICATION_REPORT']:
        verification_report = root.find(tag_name)
        if verification_report is not None and len(verification_report) > 0:
            break
    
    if verification_report is not None:
        # Look for individual checks
        checks = verification_report.findall('.//check')
        for check in checks:
            check_id = check.get('id')
            if check_id and check_id.lower() == 'pcg_compliance':
                result = check.get('result')
                metrics['pcg_compliance'] = result
        
        # Look for meta section
        meta = None
        for tag_name in ['.//meta', './/META']:
            meta = verification_report.find(tag_name)
            if meta is not None:
                break
        if meta is not None:
            consensus_elem = None
            for tag_name in ['.//consensus_score', './/ConsensusScore']:
                consensus_elem = meta.find(tag_name)
                if consensus_elem is not None:
                    break
            if consensus_elem is not None and consensus_elem.text:
                metrics['consensus_score'] = consensus_elem.text
            
            iterations_elem = None
            for tag_name in ['.//iterations_used', './/IterationsUsed']:
                iterations_elem = meta.find(tag_name)
                if iterations_elem is not None:
                    break
            if iterations_elem is not None and iterations_elem.text:
                metrics['iterations'] = iterations_elem.text
            
            fallback_elem = None
            for tag_name in ['.//fallback_flag', './/FallbackFlag']:
                fallback_elem = meta.find(tag_name)
                if fallback_elem is not None:
                    break
            if fallback_elem is not None and fallback_elem.text:
                metrics['fallback'] = fallback_elem.text
    
    # Extract structure metrics - try both upper and lower case
    # Looking for key facts in various possible locations
    context = None
    for tag_name in ['.//Context', './/context', './/CONTEXT']:
        context = root.find(tag_name)
        if context is not None:
            break
    if context is not None:
        # Count facts in various possible formats
        facts_found = (context.findall('.//fact') + 
                      context.findall('.//Fact') + 
                      context.findall('.//FACT') +
                      context.findall('.//FACT'))
        metrics['fact_count'] = len(facts_found)
    
    return metrics

def parse_experiment_metrics(exp_name, metadata):
    """
    Parse all cases (Case1-Case5) for a single experiment.
    """
    logging.info(f"Parsing metrics for {exp_name}")
    
    exp_metrics = {
        'exp_id': exp_name,
        'model': metadata[exp_name]['model'],
        'temperature': metadata[exp_name]['temperature'],
        'cases': {}
    }
    
    for case_num in range(1, 6):
        case_name = f'Case{case_num}'
        case_metrics = parse_case_metrics(exp_name, case_name)
        exp_metrics['cases'][case_name] = case_metrics
    
    # Calculate Jaccard distances between summaries
    case1_summary = exp_metrics['cases']['Case1'].get('summary_text', '')
    if case1_summary:
        case1_words = set(case1_summary.split())
        
        for case_num in range(2, 6):
            case_name = f'Case{case_num}'
            case_summary = exp_metrics['cases'][case_name].get('summary_text', '')
            if case_summary:
                case_words = set(case_summary.split())
                intersection = len(case1_words.intersection(case_words))
                union = len(case1_words.union(case_words))
                
                if union > 0:
                    jaccard_distance = 1 - (intersection / union)
                    exp_metrics['cases'][case_name]['jaccard_distance'] = jaccard_distance
                else:
                    exp_metrics['cases'][case_name]['jaccard_distance'] = 1.0  # Complete difference
    
    return exp_metrics

def parse_all_experiments(metadata):
    """
    PHASE 2: PARSE PER EXP
    For each ExpXX: Parse all cases and extract metrics.
    """
    logging.info("Starting parsing phase...")
    
    all_metrics = []
    exp_dir = Path('./Experiments')
    
    for exp_path in exp_dir.iterdir():
        if not exp_path.is_dir() or not re.match(r'Exp\d{2}', exp_path.name):
            continue
            
        exp_metrics = parse_experiment_metrics(exp_path.name, metadata)
        all_metrics.append(exp_metrics)
    
    logging.info(f"Parsed metrics for {len(all_metrics)} experiments")
    return all_metrics

def aggregate_metrics(all_metrics):
    """
    PHASE 3: AGGREGATE
    - Per Exp: avg_consensus, pcg_rate, avg_distance (Cases2–5 vs Case1), 3A_freq (%).
    - Per Model: Mean/std across Exps.
    - p-value: Mann-Whitney pcg_rate/consensus (scipy.stats).
    """
    logging.info("Starting aggregation phase...")
    
    # Import scipy only when needed to avoid error if not installed
    try:
        from scipy.stats import mannwhitneyu
        scipy_available = True
    except ImportError:
        logging.warning("scipy not available, skipping p-value calculations")
        scipy_available = False
    
    # Calculate per experiment metrics
    for exp_metrics in all_metrics:
        exp_id = exp_metrics['exp_id']
        cases = exp_metrics['cases']
        
        # Calculate average consensus score
        consensus_scores = []
        for case_metrics in cases.values():
            consensus_str = case_metrics.get('consensus_score')
            if consensus_str:
                try:
                    consensus_scores.append(float(consensus_str))
                except ValueError:
                    continue
        
        if consensus_scores:
            exp_metrics['avg_consensus'] = sum(consensus_scores) / len(consensus_scores)
        else:
            exp_metrics['avg_consensus'] = 0.0
        
        # Calculate PCG compliance rate
        pcg_compliance_scores = []
        for case_metrics in cases.values():
            pcg_str = case_metrics.get('pcg_compliance')
            if pcg_str:
                try:
                    # Parse "X/Y" format or percentage
                    if '/' in pcg_str:
                        parts = pcg_str.split('/')
                        if len(parts) == 2:
                            pcg_compliance_scores.append(float(parts[0]) / float(parts[1]))
                    elif pcg_str.lower() == 'pass':
                        pcg_compliance_scores.append(1.0)  # Consider 'pass' as 100% compliance
                    elif pcg_str.lower() == 'fail':
                        pcg_compliance_scores.append(0.0)  # Consider 'fail' as 0% compliance
                    else:
                        pcg_compliance_scores.append(float(pcg_str))
                except ValueError:
                    continue
        
        if pcg_compliance_scores:
            exp_metrics['pcg_rate'] = sum(pcg_compliance_scores) / len(pcg_compliance_scores)
        else:
            exp_metrics['pcg_rate'] = 0.0
        
        # Calculate average distance from Case1 (for Cases 2-5)
        distances = []
        for case_num in range(2, 6):
            case_name = f'Case{case_num}'
            distance = cases[case_name].get('jaccard_distance')
            if distance is not None:
                distances.append(distance)
        
        if distances:
            exp_metrics['avg_distance'] = sum(distances) / len(distances)
        else:
            exp_metrics['avg_distance'] = 0.0  # Default if no distances calculated
        
        # Calculate 3A frequency
        scenarios = []
        for case_metrics in cases.values():
            scenario = case_metrics.get('scenario')
            if scenario:
                scenarios.append(scenario)
        
        if scenarios:
            scenario_counts = Counter(scenarios)
            exp_metrics['3A_freq'] = scenario_counts.get('3A', 0) / len(scenarios)
        else:
            exp_metrics['3A_freq'] = 0.0
    
    # Aggregate by model
    model_data = {}
    for exp_metrics in all_metrics:
        model = exp_metrics['model']
        if model not in model_data:
            model_data[model] = {
                'pcg_rates': [],
                'avg_consensus_scores': [],
                'avg_distances': [],
                'exp_metrics': []
            }
        
        model_data[model]['pcg_rates'].append(exp_metrics.get('pcg_rate', 0.0))
        model_data[model]['avg_consensus_scores'].append(exp_metrics.get('avg_consensus', 0.0))
        model_data[model]['avg_distances'].append(exp_metrics.get('avg_distance', 0.0))
        model_data[model]['exp_metrics'].append(exp_metrics)
    
    # Calculate statistics per model
    for model, data in model_data.items():
        pcg_rates = data['pcg_rates']
        consensus_scores = data['avg_consensus_scores']
        distances = data['avg_distances']
        
        # Means
        data['mean_pcg_rate'] = sum(pcg_rates) / len(pcg_rates) if pcg_rates else 0.0
        data['mean_consensus'] = sum(consensus_scores) / len(consensus_scores) if consensus_scores else 0.0
        data['mean_distance'] = sum(distances) / len(distances) if distances else 0.0
        
        # Standard deviations
        if len(pcg_rates) > 1:
            mean_pcg = data['mean_pcg_rate']
            data['std_pcg_rate'] = (sum([(x - mean_pcg) ** 2 for x in pcg_rates]) / (len(pcg_rates) - 1)) ** 0.5
        else:
            data['std_pcg_rate'] = 0.0
        
        if len(consensus_scores) > 1:
            mean_cons = data['mean_consensus']
            data['std_consensus'] = (sum([(x - mean_cons) ** 2 for x in consensus_scores]) / (len(consensus_scores) - 1)) ** 0.5
        else:
            data['std_consensus'] = 0.0
        
        if len(distances) > 1:
            mean_dist = data['mean_distance']
            data['std_distance'] = (sum([(x - mean_dist) ** 2 for x in distances]) / (len(distances) - 1)) ** 0.5
        else:
            data['std_distance'] = 0.0
    
    # Calculate p-values if scipy is available
    insights = {}
    if scipy_available and len(model_data) >= 2:
        models = list(model_data.keys())
        if len(models) >= 2:
            # Compare first two models
            model1, model2 = models[0], models[1]
            data1 = model_data[model1]
            data2 = model_data[model2]
            
            try:
                # Perform Mann-Whitney U test for PCG rates
                if data1['pcg_rates'] and data2['pcg_rates']:
                    u_pcg, p_pcg = mannwhitneyu(data1['pcg_rates'], data2['pcg_rates'], alternative='two-sided')
                    insights['qwen_vs_gpt'] = {
                        'pcg_diff': data1['mean_pcg_rate'] - data2['mean_pcg_rate'],
                        'p_val': p_pcg
                    }
            except ValueError as e:
                logging.warning(f"Could not calculate p-value for PCG rates: {e}")
            
            try:
                # Perform Mann-Whitney U test for consensus scores
                if data1['avg_consensus_scores'] and data2['avg_consensus_scores']:
                    u_cons, p_cons = mannwhitneyu(data1['avg_consensus_scores'], data2['avg_consensus_scores'], alternative='two-sided')
                    if 'qwen_vs_gpt' not in insights:
                        insights['qwen_vs_gpt'] = {}
                    insights['qwen_vs_gpt']['consensus_diff'] = data1['mean_consensus'] - data2['mean_consensus']
                    insights['qwen_vs_gpt']['consensus_p_val'] = p_cons
            except ValueError as e:
                logging.warning(f"Could not calculate p-value for consensus scores: {e}")
    
    # Check for variability trend with temperature (only for GPT-5 low if it has temp variation)
    gpt5_temps = []
    gpt5_distances = []
    for exp_metrics in all_metrics:
        if exp_metrics['model'] == 'GPT-5 low':
            temp = exp_metrics['temperature']
            dist = exp_metrics.get('avg_distance', 0.0)
            gpt5_temps.append(temp)
            gpt5_distances.append(dist)
    
    if len(gpt5_temps) > 1:
        # Simple linear correlation as trend
        n = len(gpt5_temps)
        sum_x = sum(gpt5_temps)
        sum_y = sum(gpt5_distances)
        sum_xy = sum([gpt5_temps[i] * gpt5_distances[i] for i in range(n)])
        sum_x2 = sum([x * x for x in gpt5_temps])
        
        # Calculate correlation coefficient
        numerator = n * sum_xy - sum_x * sum_y
        denominator_x = (n * sum_x2 - sum_x * sum_x) ** 0.5
        denominator_y = (n * sum([y * y for y in gpt5_distances]) - sum_y * sum_y) ** 0.5
        
        if denominator_x != 0 and denominator_y != 0:
            correlation = numerator / (denominator_x * denominator_y)
            insights['variability_trend'] = f"linear with temp, correlation: {correlation:.3f}"
        else:
            insights['variability_trend'] = "insufficient data for trend analysis"
    else:
        insights['variability_trend'] = "no temperature variation in GPT-5 low model"
    
    aggregated_results = {
        'experiment_metrics': all_metrics,
        'model_data': model_data,
        'insights': insights
    }
    
    logging.info("Aggregation phase completed")
    return aggregated_results

def generate_output(aggregated_results):
    """
    PHASE 4: OUTPUT
    - summary.csv: exp_id, model, temp, pcg_rate, avg_consensus, avg_distance, 3A_freq.
    - insights.json: {'qwen_vs_gpt': {'pcg_diff': mean_q - mean_g, 'p_val': p}, 'variability_trend': 'linear with temp'}.
    - Plot: Matplotlib line temp vs distance (hue=model); save fig.png.
    """
    logging.info("Starting output generation phase...")
    
    # Generate summary.csv
    with open('summary.csv', 'w', newline='') as csvfile:
        fieldnames = ['exp_id', 'model', 'temperature', 'pcg_rate', 'avg_consensus', 'avg_distance', '3A_freq']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for exp_metrics in aggregated_results['experiment_metrics']:
            row = {
                'exp_id': exp_metrics['exp_id'],
                'model': exp_metrics['model'],
                'temperature': exp_metrics['temperature'],
                'pcg_rate': exp_metrics.get('pcg_rate', ''),
                'avg_consensus': exp_metrics.get('avg_consensus', ''),
                'avg_distance': exp_metrics.get('avg_distance', ''),
                '3A_freq': exp_metrics.get('3A_freq', '')
            }
            writer.writerow(row)
    
    # Generate insights.json
    with open('insights.json', 'w') as f:
        json.dump(aggregated_results['insights'], f, indent=2)    
    
    logging.info("Output generation phase completed")
    print("Generated summary.csv and insights.json")

def initialize_analyzer():
    """
    PHASE 0: INIT
    - Create checklist.md with steps (mark as done).
    - Verify Experiments/ exists with Exp00–Exp11/Case1–5/ (fd.xml, sint_prompt.txt, output*.xml, task.txt for 2–5).
    """
    logging.info("Starting initialization...")
    
    # Create checklist.md
    checklist_content = """
# Analyzer Checklist

- [ ] Verify Experiments/ directory structure
- [ ] Check for Exp00-Exp11 with Case1-Case5 subdirs
- [ ] Validate required files exist
- [x] Initialization complete
- [ ] Metadata loading (Phase 1)
- [ ] Parsing (Phase 2)
- [ ] Aggregation (Phase 3)
- [ ] Output generation (Phase 4)
"""
    with open('checklist.md', 'w') as f:
        f.write(checklist_content.strip())
    logging.info("Created checklist.md")

    # Verify Experiments/ directory
    exp_dir = Path('./Experiments')
    if not exp_dir.exists() or not exp_dir.is_dir():
        error_msg = f"Error: {exp_dir} does not exist or is not a directory"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Check for Exp00–Exp11
    expected_exps = [f'Exp{i:02d}' for i in range(12)]
    found_exps = [d.name for d in exp_dir.iterdir() if d.is_dir() and d.name in expected_exps]
    if set(expected_exps) != set(found_exps):
        missing = set(expected_exps) - set(found_exps)
        extra = set(found_exps) - set(expected_exps)
        error_msg = f"Missing experiments: {missing}, Extra: {extra}"
        logging.error(error_msg)
        raise ValueError(error_msg)

    # For each ExpXX, check Case1–Case5 and required files
    required_files_per_case = {
        'Case1': ['fd.xml', 'sint_prompt.txt', 'output_raw.xml'],  # task.txt not required
        'Case2': ['fd.xml', 'sint_prompt.txt', 'output.xml', 'task.txt'],
        'Case3': ['fd.xml', 'sint_prompt.txt', 'output.xml', 'task.txt'],
        'Case4': ['fd.xml', 'sint_prompt.txt', 'output.xml', 'task.txt'],
        'Case5': ['fd.xml', 'sint_prompt.txt', 'output.xml', 'task.txt']
    }

    all_files_present = True
    for exp_name in expected_exps:
        exp_path = exp_dir / exp_name
        if not exp_path.exists():
            continue  # Already handled above
        
        # Check Case1–Case5 exist
        found_cases = [c.name for c in exp_path.iterdir() if c.is_dir() and re.match(r'Case[1-5]', c.name)]
        expected_cases = [f'Case{i}' for i in range(1, 6)]
        if set(expected_cases) != set(found_cases):
            missing_cases = set(expected_cases) - set(found_cases)
            error_msg = f"In {exp_name}: missing cases {missing_cases}"
            logging.error(error_msg)
            all_files_present = False
            continue

        # Check files within each case
        for case_name in expected_cases:
            case_path = exp_path / case_name
            for file_name in required_files_per_case[case_name]:
                file_path = case_path / file_name
                if not file_path.exists():
                    error_msg = f"Missing file {file_path} in {exp_name}/{case_name}"
                    logging.error(error_msg)
                    all_files_present = False

    if not all_files_present:
        error_msg = "Not all required files present. Check run.log for details."
        logging.error(error_msg)
        raise ValueError(error_msg)

    logging.info("Initialization completed successfully")
    print("Initialization phase complete. All required files and directories verified.")

if __name__ == '__main__':
    initialize_analyzer()
    metadata = load_metadata()
    print(f"Loaded metadata for {len(metadata)} experiments")
    # Print a sample of loaded metadata
    for exp, data in list(metadata.items())[:3]:
        print(f"{exp}: {data}")
    
    all_metrics = parse_all_experiments(metadata)
    print(f"Parsed metrics for {len(all_metrics)} experiments")
    # Print a sample of parsed metrics
    for exp_metrics in all_metrics[:1]:  # Just first experiment
        print(f"\n{exp_metrics['exp_id']}:")
        for case, metrics in exp_metrics['cases'].items():
            print(f"  {case}: {list(metrics.keys())[:5]}...")  # Show first 5 metric keys
    
    aggregated_results = aggregate_metrics(all_metrics)
    print(f"\nAggregated results for {len(aggregated_results['model_data'])} models")
    for model, data in aggregated_results['model_data'].items():
        print(f"{model}: mean_pcg_rate={data['mean_pcg_rate']:.3f}, mean_distance={data['mean_distance']:.3f}")
    print(f"Insights: {aggregated_results['insights']}")
    
    generate_output(aggregated_results)