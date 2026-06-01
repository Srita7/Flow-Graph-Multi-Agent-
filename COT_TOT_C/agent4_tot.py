from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import os
import json
from typing import Dict, Any

# Optional Gemini (EXACT SAME STYLE AS AGENT 1–3)
try:
    import google.generativeai as genai
    HAS_GENAI = True
    print(" Gemini imported")
except ImportError:
    genai = None
    HAS_GENAI = False
    print(" Gemini not available")

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------- PATH CONFIG ----------------
BASE_DIR = Path(__file__).parent


INPUT_CODE_DIR = (BASE_DIR / "input_path/ansible_input_path_C").resolve()
AGENT3_DIR = (BASE_DIR / "agent3_results_tot/ansible_agent3_rectified_graph").resolve()
OUTPUT_DIR = (BASE_DIR / "agent4_results_tot/ansible_agent4_output_code").resolve()


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# --------------------------------------------

# FIXED: Properly escaped AGENT4_PROMPT
AGENT4_PROMPT = r"""
SOURCE CODE SURGICAL RECONSTRUCTION AGENT - TREE OF THOUGHT MODE

You are Agent-4.

Agent-3 has repaired the PROGRAM GRAPH.
Your responsibility is to reflect ONLY those structural repairs
into the ORIGINAL Python file.

You behave as a deterministic patching engine.

You MUST reason using multi-branch evaluation internally.
DO NOT output reasoning.
OUTPUT ONLY THE FINAL C FILE.

--------------------------------------------------
PRIMARY LAW

The ORIGINAL file is the ground truth.
If not required by a rectified node → DO NOT TOUCH.

--------------------------------------------------
INPUTS

=== ORIGINAL PYTHON CODE (AUTHORITATIVE) ===
{original_code}

=== RECTIFIED NODES (ONLY THESE MAY CHANGE) ===
{rectified_nodes}

=== RECTIFIED GRAPH (CONTEXT ONLY) ===
{rectified_graph}

--------------------------------------------------
TREE OF THOUGHT PATCHING PROCESS (INTERNAL ONLY)

For EACH rectified node:

PHASE 1 — LOCALIZATION
• Identify exact line span in original code
• Identify variables involved
• Identify structural intent of graph repair

PHASE 2 — GENERATE MULTIPLE PATCH CANDIDATES
Generate 2–3 possible minimal edits that satisfy the repair.

Examples:
- Insert missing assignment
- Adjust return expression
- Add minimal dependency variable
- Insert one required statement

Each candidate must:
• Modify smallest number of characters
• Preserve indentation
• Preserve formatting
• Preserve ordering

PHASE 3 — SCORE CANDIDATES
Evaluate each candidate using:

✓ Minimal edit distance
✓ No unrelated changes
✓ No refactoring
✓ No renaming
✓ No formatting change
✓ Structural correctness

Reject any candidate that:
✗ rewrites entire block
✗ changes whitespace globally
✗ modifies unrelated lines
✗ alters comments

PHASE 4 — SELECT MINIMAL SAFE PATCH
Choose the patch with:

• Smallest modification footprint
• Exact reflection of graph repair
• Maximum preservation of original file

PHASE 5 — GLOBAL VALIDATION

After applying ALL patches:

Verify:
✓ All original non-rectified lines are byte-identical
✓ File structure preserved
✓ No accidental indentation drift
✓ No syntax break
✓ All rectified nodes reflected

If uncertain → choose smaller change.

--------------------------------------------------
GLOBAL HARD CONSTRAINTS

You MUST:
✓ output COMPLETE file
✓ preserve whitespace
✓ preserve blank lines
✓ preserve comments
✓ preserve ordering

You MUST NOT:
✗ refactor
✗ optimize
✗ rename variables
✗ rewrite blocks
✗ change formatting
✗ improve style

If multiple fixes overlap → apply minimal combined patch.

--------------------------------------------------
OUTPUT RULES

Return ONLY the final Python program.
No markdown.
No explanations.
No headers.
No diff.
No reasoning.
"""


def generate_fixed_code(original_code: str, agent3_result: Dict[str, Any]) -> str:
    if not HAS_GENAI or not GEMINI_API_KEY:
        raise RuntimeError("Gemini API not available")

    rectified_nodes = json.dumps(
        agent3_result.get("rectified_nodes", []),
        indent=2
    )

    rectified_graph = agent3_result.get("full_rectified_graph", "")

    prompt = AGENT4_PROMPT.format(
        original_code=original_code,
        rectified_nodes=rectified_nodes,
        rectified_graph=rectified_graph
    )

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 8000
        }
    )

    return response.text.strip()

def run_agent4():
    print("\n AGENT4: FINAL SOURCE CODE RECONSTRUCTION")
    # print(f" Input:   {INPUT_CODE_DIR.absolute()}")
    # print(f" Agent3:  {AGENT3_DIR.absolute()}")
    # print(f" Output:  {OUTPUT_DIR.absolute()}")

    py_files = list(INPUT_CODE_DIR.glob("*.c"))
    print(f" Found {len(py_files)} input .c files")
    
    processed = 0
    skipped = 0
    
    for py_file in py_files:
        file_stem = py_file.stem  # e.g., "bug1"
        
        # ✅ FIXED: Exact Agent3 filename from your screenshot
        agent3_json = AGENT3_DIR / f"{file_stem}.blocks_graph_agent3_full.json"
        
        if not agent3_json.exists():
            print(f" Skipping {file_stem}: Missing {agent3_json.name}")
            skipped += 1
            continue

        print(f"\n Processing {file_stem}.c")
        print(f"    Agent3 JSON: {agent3_json.name}")
        
        # Read original code
        original_code = py_file.read_text(encoding="utf-8", errors="ignore").strip()
        
        # Load Agent3 results
        try:
            with agent3_json.open("r", encoding="utf-8") as f:
                agent3_result = json.load(f)
            fixes = len(agent3_result.get('rectified_nodes', []))
            print(f"    {fixes} graph fixes loaded")
        except Exception as e:
            print(f" JSON load error: {e}")
            skipped += 1
            continue

        # Generate fixed code
        try:
            fixed_code = generate_fixed_code(original_code, agent3_result)
            
            out_file = OUTPUT_DIR / f"{file_stem}.c"
            out_file.write_text(fixed_code, encoding="utf-8")
            
            print(f"CREATED: {out_file.name}")
            processed += 1
            
        except Exception as e:
            print(f"Gemini generation failed: {e}")
            skipped += 1
            continue

    print(f"\n AGENT4 PIPELINE COMPLETE!")
    # print(f" Processed: {processed}/{len(py_files)} files")
    # print(f" Skipped:   {skipped} files")
    # print(f" Results:    {OUTPUT_DIR.absolute()}")

if __name__ == "__main__":
    run_agent4()
