# SINT v2.2: Synthesized Iterative Network of Thought

**Authors:** Vladimir Sitnikov, Anna Sitnikova  
**Affiliation:** Independent Researchers, Bar, Montenegro  
**Date:** 2025  
**Repository:** [https://github.com/ais-space/SINT](https://github.com/ais-space/SINT)  
**License:** MIT License

---

## Abstract

**SINT v2.2** is a multi-agent analytical framework for structured reasoning with large language models (LLM) that **requires no prompt-engineering skills** — users describe tasks in natural language, and the **System Designer** automatically formalizes them.

It introduces **architectural guarantees** of:
- **Traceability** via **Principle of Contextual Grounding (PCG)**  
- **Pre-validation** (Step 0 — prevents infeasible tasks)  
- **Deterministic conflict resolution**  
- **Machine-readable XML output** with mandatory **Verification Report**

SINT v2.2 ensures **reproducible results even on non-flagship models**, making it suitable for industrial-grade AI systems.

**Keywords:** prompt-engineering, multi-agent systems, XML reasoning, contextual grounding, reproducible AI
---

## Preprint

**PDF (RU & EN), LaTeX sources, and bibliography:**  
→ [https://doi.org/10.5281/zenodo.17410094](https://doi.org/10.5281/zenodo.17410094)

**All files are in this repository.**

---

## Repository Structure

```
SINT/
├── SINT_RU.pdf                  # Russian preprint
├── SINT_EN.pdf                  # English preprint
├── SINT_RU.tex                  # LaTeX source (RU)
├── SINT_EN.tex                  # LaTeX source (EN)
├── refs.bib                     # Bibliography
├── SP1_Designer_Chat_EN.md
├── SP1_Designer_Chat_RU.md
├── SP1_Designer_CLI_EN.md
├── SP1_Designer_CLI_RU.md
├── SP2_Coder_Chat_EN.md
├── SP2_Coder_Chat_RU.md
├── SP2_Coder_CLI_EN.md
├── SP2_Coder_CLI_RU.md
├── Cascade_CLI_EN.md            # Automated Cascade Processor (English)
├── Cascade_CLI_RU.md            # Automated Cascade Processor (Russian)
├── analyzer.py                  # Reproducibility analysis
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
├── README.md                    # This file
├── .gitignore
├── Examples/                    # Example tasks and prompts
│   ├── Case1/                   # Task generator
│   ├── Case2/                   # Debate + Conflict
│   ├── Case3/                   # Debate + Consensus
│   ├── Case4/                   # Generator-Critic
│   └── Case5/                   # Multi-stakeholder
└── Experiments/                 # 12 experiments (Exp00–Exp11)
    ├── Exp00/
    │   ├── Case1/
    │   ├── Case2/
    │   └── ...
    └── ...
```

---

## Reproducibility

Run the analysis locally:

```bash
pip install -r requirements.txt
python3 analyzer.py
```

**Generates (in your local directory):**
- `summary.csv` — per-experiment metrics
- `insights.json` — statistical insights
- `run.log` — execution log
- `checklist.md` — verification status

**Verified Results (from paper):**
- PCG = 1.000 (both models)
- Jaccard distance = 0.000
- Consensus: GPT-5 low = 7.25, Qwen3-Coder = 5.36

---

## Citation

```bibtex
@misc{sitnikov2025sint,
  title={SINT v2.2: Synthesized Iterative Network of Thought},
  author={Sitnikov, Vladimir and Sitnikova, Anna},
  year={2025},
  publisher={Zenodo},
  doi={10.5281/zenodo.17410094},
  url={https://doi.org/10.5281/zenodo.17410094},
  note={Preprint with full reproducibility suite}
}
```

---

## Release Contents (Zenodo)

The **Zenodo release** includes:
- `SINT_RU.pdf`
- `SINT_EN.pdf`
- `SINT_RU.tex`
- `SINT_EN.tex`
- `refs.bib`
- `LICENSE`
- `README.md`

All other files (prompts, examples, experiments, analyzer) are available in the **GitHub repository**.

---

## Purpose

This repository is a **living preprint archive** and **reproducibility hub**. It preserves authorship priority and provides executable proof of all claims.

Future releases will include:
- Interactive Jupyter notebooks
- Docker container
- Web demo