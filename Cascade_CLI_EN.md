SINT V2.2: Universal Interactive Cascade Processor (5 Cases)

PURPOSE: Ensures interactive generation, execution, and archiving of 5 SINT cases in dialogue mode.
LANGUAGE: All generated documents (tasks, FD, SINT prompts, output) MUST BE in English.
MODE: Executed in interactive environment (dialogue system).

# -----------------------------------------------------------------------------
# PHASE 0: INITIALIZATION AND READINESS CHECK
# -----------------------------------------------------------------------------

Action 0.0: Create execution checklist file
Description: Check for the existence of the auxiliary file checklist.md. If it exists, clear its content; if not, create it. Fill it with a detailed hierarchical list of steps for executing this prompt with checkboxes for marking completion of each step.
Expected result: The checklist.md file exists and is properly filled
CHECK: Ensure checklist.md exists and is properly filled
IMPORTANT: Always and only after completing each step, mark the completed step in the checklist file
Additionally: Check the checklist

Action 0.1: Root directory creation
Description: Create the MyCases directory if it does not exist
Expected result: MyCases directory exists
CHECK: Ensure the MyCases directory exists
Additionally: Check the checklist

Action 0.2: Prompt files verification
Description: Ensure that SP1_Designer_CLI_EN.md and SP2_Coder_CLI_EN.md files are available in the system
Expected result: Prompt files exist and are accessible
IMPORTANT: If files are missing, the process should not continue
Additionally: Check the checklist

Action 0.3: MyCases directory cleanliness check
Description: Ensure that the MyCases directory does not contain results from previous runs, if the run is from scratch
Expected result: Prepared clean execution environment
Additionally: Check the checklist

Action 0.4: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

# -----------------------------------------------------------------------------
# PHASE 1: ENVIRONMENT AND VARIABLE SETUP
# -----------------------------------------------------------------------------

Action 1.1: Subdirectories preparation
Description: Create 5 subdirectories in MyCases/: Case1, Case2, Case3, Case4, Case5
Expected result: All 5 subdirectories exist
CHECK: Ensure all 5 subdirectories are created
Additionally: Check the checklist

# META_TASK_INPUT: Content of the first task (Case 1), embedded for script autonomy.
# Explicitly instructs the LLM to generate all output in English.

META_TASK_INPUT_CONTENT:
Request Type: System Design Request (SINT System Designer V2.2)
Project Name: Generation of Diverse Complex Analytical Tasks
Customer: SINT Research Laboratory
1.0. Objective: Generate a single, detailed, and technically complete Formal Definition (FD), which will be used by the 'Code Generator' agent to create a SINT prompt that in turn should generate 4 different complex analytical tasks, each requiring a unique interdisciplinary approach with detailed expert analysis, numerical ratings, iterative convergence, and comprehensive synthesis.
2.0. Context: The generated tasks should cover fundamentally different areas of knowledge, require various sets of experts and methodologies, demonstrate the broad spectrum of SINT framework capabilities, and require highly detailed analysis with numerical ratings and iterative synthesis.
2.3.2. Task Specification (Generation Result): The 4 generated tasks must strictly demonstrate the following SINT modes: Task 1 (Case 2): Debates (N=3) + Conflict (Step 3A) with detailed expert positions, numerical ratings (1-10), cross-criticism, and iterative convergence. Task 2 (Case 3): Debates (N=3) + Consensus (Step 3B) with structured rating system, detailed arguments, and multi-round synthesis. Task 3 (Case 4): Generator + Critic (N=2) with comprehensive feedback loops and detailed analysis. Task 4 (Case 5): Debates (N=4) + Conflict (Step 3A) with numerical ratings, cross-evaluation, and iterative synthesis.
3.0. Constraints: Each of the 4 tasks must require a separate full SINT application. All tasks must be fundamentally different in thematic and approaches. All tasks must be formulated considering the principle of contextual grounding (PCG). Each task must have clearly defined objectives and expected outcomes. All expert positions must include detailed arguments, numerical ratings (1-10), cross-evaluation scores, and specific examples. The output must include multiple rounds of criticism, iterative convergence, and comprehensive synthesis.
4.0. Language Constraint: All output (including 4 generated tasks) MUST BE in English.
4.1. Analysis Requirements: Each expert must provide detailed, specific arguments with concrete examples, data points, and numerical ratings. The process must include iterative rounds of criticism and synthesis with detailed cross-evaluation between experts.

# -----------------------------------------------------------------------------
# PHASE 2: FULL SINT CYCLE FOR CASE 1 (SPECIAL CASE)
# WARNING: Case1 uses META_TASK_INPUT_CONTENT directly in SP1, not task.txt
# WARNING: From Case1 result (output_raw.xml), 4 tasks will be extracted for Cases 2-5
# -----------------------------------------------------------------------------

Action 2.1: Launch SP1 (System Designer) for Case 1
Input data:
- SP1_Designer_CLI_EN.md (Prompt 1)
- META_TASK_INPUT_CONTENT (content from the above block)
Description:
- Load the content of SP1_Designer_CLI_EN.md
- Process META_TASK_INPUT_CONTENT with SP1_Designer
- Save the result to MyCases/Case1/fd.xml
Expected result: File MyCases/Case1/fd.xml contains the formalized task created by SP1_Designer based on META_TASK_INPUT_CONTENT
CHECK: Ensure MyCases/Case1/fd.xml exists
Additionally: Check the checklist

Action 2.2: Launch SP2 (Code Generator) for Case 1
Input data:
- SP2_Coder_CLI_EN.md (Prompt 2)
- MyCases/Case1/fd.xml (result of Action 2.1)
Description:
- Load the content of SP2_Coder_CLI_EN.md
- Load the content of MyCases/Case1/fd.xml
- Execute session 2 (SINT Code Generator) with fd.xml as input data
- Save the result to MyCases/Case1/sint_prompt.txt
Expected result: File MyCases/Case1/sint_prompt.txt contains the SINT prompt for Case1
CHECK: Ensure MyCases/Case1/sint_prompt.txt exists
Additionally: Check the checklist

Action 2.3: Launch Executor for Case 1
Input data:
- MyCases/Case1/sint_prompt.txt (result of Action 2.2)
Description:
- Load the content of MyCases/Case1/sint_prompt.txt
- Execute session 3 (SINT Executor) with the prompt
- Save the result to MyCases/Case1/output_raw.xml
Expected result: File MyCases/Case1/output_raw.xml contains execution results, including 4 additional tasks
CHECK: Ensure MyCases/Case1/output_raw.xml exists
Additionally: Check the checklist

Action 2.4: Parse 4 tasks and save to task.txt files (Cases 2-5)
Input data:
- MyCases/Case1/output_raw.xml (result of Action 2.3)
Description:
- Extract 4 separate tasks from MyCases/Case1/output_raw.xml
- Save task 1 to MyCases/Case2/task.txt
- Save task 2 to MyCases/Case3/task.txt
- Save task 3 to MyCases/Case4/task.txt
- Save task 4 to MyCases/Case5/task.txt
Expected result: 4 task.txt files are created with corresponding tasks (for Cases 2-5)
CHECK: Ensure all 4 task.txt files (for Cases 2-5) exist and contain tasks
Additionally: Check the checklist

Action 2.5: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

# -----------------------------------------------------------------------------
# PHASE 3: FULL SINT CYCLES FOR REMAINING CASES (2-5)
# WARNING: Execute each sub-phase ONLY AFTER completing the previous one
# WARNING: Each sub-phase uses ITS OWN task.txt file (Cases 2-5)
# WARNING: Case1 is already completed, this phase serves only Cases 2-5
# -----------------------------------------------------------------------------

# SUB-PHASE 3.1: Processing Case 2
# INPUT DATA: MyCases/Case2/task.txt (extracted from MyCases/Case1/output_raw.xml in phase 2.4)
Action 3.1.1: Launch SP1 (System Designer) for Case 2
Input data:
- MyCases/Case2/task.txt (result of Action 2.4)
- SP1_Designer_CLI_EN.md (Prompt 1)
Description:
- Load the content of MyCases/Case2/task.txt
- Load the content of SP1_Designer_CLI_EN.md
- Execute session 1 (SINT System Designer) with task.txt as input data
- Save the result to MyCases/Case2/fd.xml
Expected result: File MyCases/Case2/fd.xml contains the results of session 1 for task 2
CHECK: Ensure MyCases/Case2/fd.xml exists
Additionally: Check the checklist

Action 3.1.2: Launch SP2 (Code Generator) for Case 2
Input data:
- MyCases/Case2/fd.xml (result of Action 3.1.1)
- SP2_Coder_CLI_EN.md (Prompt 2)
Description:
- Load the content of MyCases/Case2/fd.xml
- Load the content of SP2_Coder_CLI_EN.md
- Execute session 2 (SINT Code Generator) with fd.xml as input data
- Save the result to MyCases/Case2/sint_prompt.txt
Expected result: File MyCases/Case2/sint_prompt.txt contains the SINT prompt for task 2
CHECK: Ensure MyCases/Case2/sint_prompt.txt exists
Additionally: Check the checklist

Action 3.1.3: Launch Executor for Case 2
Input data:
- MyCases/Case2/sint_prompt.txt (result of Action 3.1.2)
Description:
- Load the content of MyCases/Case2/sint_prompt.txt
- Execute session 3 (SINT Executor) with the prompt
- Save the result to MyCases/Case2/output.xml
Expected result: File MyCases/Case2/output.xml contains the final result for task 2
CHECK: Ensure MyCases/Case2/output.xml exists
Additionally: Check the checklist

Action 3.1.4: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

# SUB-PHASE 3.2: Processing Case 3
# INPUT DATA: MyCases/Case3/task.txt (extracted from MyCases/Case1/output_raw.xml in phase 2.4)
Action 3.2.1: Launch SP1 (System Designer) for Case 3
Input data:
- MyCases/Case3/task.txt (result of Action 2.4)
- SP1_Designer_CLI_EN.md (Prompt 1)
Description:
- Load the content of MyCases/Case3/task.txt
- Load the content of SP1_Designer_CLI_EN.md
- Execute session 1 (SINT System Designer) with task.txt as input data
- Save the result to MyCases/Case3/fd.xml
Expected result: File MyCases/Case3/fd.xml contains the results of session 1 for task 3
CHECK: Ensure MyCases/Case3/fd.xml exists
Additionally: Check the checklist

Action 3.2.2: Launch SP2 (Code Generator) for Case 3
Input data:
- MyCases/Case3/fd.xml (result of Action 3.2.1)
- SP2_Coder_CLI_EN.md (Prompt 2)
Description:
- Load the content of MyCases/Case3/fd.xml
- Load the content of SP2_Coder_CLI_EN.md
- Execute session 2 (SINT Code Generator) with fd.xml as input data
- Save the result to MyCases/Case3/sint_prompt.txt
Expected result: File MyCases/Case3/sint_prompt.txt contains the SINT prompt for task 3
CHECK: Ensure MyCases/Case3/sint_prompt.txt exists
Additionally: Check the checklist

Action 3.2.3: Launch Executor for Case 3
Input data:
- MyCases/Case3/sint_prompt.txt (result of Action 3.2.2)
Description:
- Load the content of MyCases/Case3/sint_prompt.txt
- Execute session 3 (SINT Executor) with the prompt
- Save the result to MyCases/Case3/output.xml
Expected result: File MyCases/Case3/output.xml contains the final result for task 3
CHECK: Ensure MyCases/Case3/output.xml exists
Additionally: Check the checklist

Action 3.2.4: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

# SUB-PHASE 3.3: Processing Case 4
# INPUT DATA: MyCases/Case4/task.txt (extracted from MyCases/Case1/output_raw.xml in phase 2.4)
Action 3.3.1: Launch SP1 (System Designer) for Case 4
Input data:
- MyCases/Case4/task.txt (result of Action 2.4)
- SP1_Designer_CLI_EN.md (Prompt 1)
Description:
- Load the content of MyCases/Case4/task.txt
- Load the content of SP1_Designer_CLI_EN.md
- Execute session 1 (SINT System Designer) with task.txt as input data
- Save the result to MyCases/Case4/fd.xml
Expected result: File MyCases/Case4/fd.xml contains the results of session 1 for task 4
CHECK: Ensure MyCases/Case4/fd.xml exists
Additionally: Check the checklist

Action 3.3.2: Launch SP2 (Code Generator) for Case 4
Input data:
- MyCases/Case4/fd.xml (result of Action 3.3.1)
- SP2_Coder_CLI_EN.md (Prompt 2)
Description:
- Load the content of MyCases/Case4/fd.xml
- Load the content of SP2_Coder_CLI_EN.md
- Execute session 2 (SINT Code Generator) with fd.xml as input data
- Save the result to MyCases/Case4/sint_prompt.txt
Expected result: File MyCases/Case4/sint_prompt.txt contains the SINT prompt for task 4
CHECK: Ensure MyCases/Case4/sint_prompt.txt exists
Additionally: Check the checklist

Action 3.3.3: Launch Executor for Case 4
Input data:
- MyCases/Case4/sint_prompt.txt (result of Action 3.3.2)
Description:
- Load the content of MyCases/Case4/sint_prompt.txt
- Execute session 3 (SINT Executor) with the prompt
- Save the result to MyCases/Case4/output.xml
Expected result: File MyCases/Case4/output.xml contains the final result for task 4
CHECK: Ensure MyCases/Case4/output.xml exists
Additionally: Check the checklist

Action 3.3.4: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

# SUB-PHASE 3.4: Processing Case 5
# INPUT DATA: MyCases/Case5/task.txt (extracted from MyCases/Case1/output_raw.xml in phase 2.4)
Action 3.4.1: Launch SP1 (System Designer) for Case 5
Input data:
- MyCases/Case5/task.txt (result of Action 2.4)
- SP1_Designer_CLI_EN.md (Prompt 1)
Description:
- Load the content of MyCases/Case5/task.txt
- Load the content of SP1_Designer_CLI_EN.md
- Execute session 1 (SINT System Designer) with task.txt as input data
- Save the result to MyCases/Case5/fd.xml
Expected result: File MyCases/Case5/fd.xml contains the results of session 1 for task 5
CHECK: Ensure MyCases/Case5/fd.xml exists
Additionally: Check the checklist

Action 3.4.2: Launch SP2 (Code Generator) for Case 5
Input data:
- MyCases/Case5/fd.xml (result of Action 3.4.1)
- SP2_Coder_CLI_EN.md (Prompt 2)
Description:
- Load the content of MyCases/Case5/fd.xml
- Load the content of SP2_Coder_CLI_EN.md
- Execute session 2 (SINT Code Generator) with fd.xml as input data
- Save the result to MyCases/Case5/sint_prompt.txt
Expected result: File MyCases/Case5/sint_prompt.txt contains the SINT prompt for task 5
CHECK: Ensure MyCases/Case5/sint_prompt.txt exists
Additionally: Check the checklist

Action 3.4.3: Launch Executor for Case 5
Input data:
- MyCases/Case5/sint_prompt.txt (result of Action 3.4.2)
Description:
- Load the content of MyCases/Case5/sint_prompt.txt
- Execute session 3 (SINT Executor) with the prompt
- Save the result to MyCases/Case5/output.xml
Expected result: File MyCases/Case5/output.xml contains the final result for task 5
CHECK: Ensure MyCases/Case5/output.xml exists
Additionally: Check the checklist

Action 3.4.4: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

# -----------------------------------------------------------------------------
# PHASE 4: FINALIZATION AND INTEGRITY VERIFICATION
# -----------------------------------------------------------------------------

Action 4.1: Results completeness verification
Description: Ensure that all result files exist:
- For Case1: fd.xml, sint_prompt.txt, output_raw.xml (without task.txt)
- For Cases 2-5: 3 files each (fd.xml, sint_prompt.txt, output.xml)
Files to check:
- MyCases/Case1/fd.xml
- MyCases/Case1/sint_prompt.txt
- MyCases/Case1/output_raw.xml
- MyCases/Case2/fd.xml
- MyCases/Case2/sint_prompt.txt
- MyCases/Case2/output.xml
- MyCases/Case2/task.txt
- MyCases/Case3/fd.xml
- MyCases/Case3/sint_prompt.txt
- MyCases/Case3/output.xml
- MyCases/Case3/task.txt
- MyCases/Case4/fd.xml
- MyCases/Case4/sint_prompt.txt
- MyCases/Case4/output.xml
- MyCases/Case4/task.txt
- MyCases/Case5/fd.xml
- MyCases/Case5/sint_prompt.txt
- MyCases/Case5/output.xml
- MyCases/Case5/task.txt
Expected result: All 19 files exist
Additionally: Check the checklist

Action 4.2: Check execution checklist for this prompt
Description: Ensure that in checklist.md, all previous steps are marked as completed
Expected result: In the checklist, all previous steps are marked as completed

Final message: "SINT Cascade Validation successfully completed. Results saved in MyCases/."
Additionally: Check the checklist

# -----------------------------------------------------------------------------
# ERROR HANDLING AND ROLLBACK
# -----------------------------------------------------------------------------

# If an error occurs at any stage:
# 1. Record the error and cause
# 2. Clean up partially created files if necessary
# 3. Return to the last verified checkpoint
# 4. Continue execution after resolving the error cause

# -----------------------------------------------------------------------------
# ADDENDUM: INTERACTIVE USAGE
# -----------------------------------------------------------------------------

1. Start with META_TASK_INPUT
2. Execute each stage upon user request
3. All results are saved in a format suitable for dialogue
4. Proceed to the next stage only after completing the previous one and passing verification
5. Special attention to Case1: it uses META_TASK_INPUT_CONTENT directly, not task.txt

This universal prompt can be used:
- In CLI systems with dialogue support
- In interactive LLM sessions
- In command-line systems with multiple interaction support
- In any tool that supports dialogue mode operation