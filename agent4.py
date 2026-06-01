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
BASE_DIR = Path(".")

INPUT_CODE_DIR = BASE_DIR / "./input_path/pandas_input_path"
AGENT3_DIR = BASE_DIR / "./agent3_rectified_graph/pandas_agent3_rectified_graph"
OUTPUT_DIR = BASE_DIR / "./agent4_output_code/pandas_agent4_output_code"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# --------------------------------------------


AGENT4_PROMPT = r"""
You are Agent-4 in a multi-agent program repair system.

Agent-3 has already fixed the PROGRAM GRAPH.
Your task is to apply those fixes back to the SOURCE CODE.

THIS IS CRITICAL:
- You MUST output the COMPLETE Python file
- You MUST preserve ALL original lines EXACTLY
- You may ONLY change lines that correspond to rectified nodes
- Do NOT reformat, reorder, or rewrite any other code
- Do NOT add or remove blank lines
- Do NOT add comments or explanations

You are performing a SURGICAL edit.

INPUTS:

=== ORIGINAL PYTHON CODE (AUTHORITATIVE) ===
{original_code}

=== RECTIFIED NODES (ONLY THESE MAY CHANGE) ===
{rectified_nodes}

=== RECTIFIED GRAPH (FOR CONTEXT ONLY) ===
{rectified_graph}

OUTPUT RULES:
- Output ONLY valid Python code
- No markdown
- No explanations
- No diffs
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
            "max_output_tokens": 6000
        }
    )

    return response.text.strip()


def run_agent4():
    print("\n AGENT4: FINAL SOURCE CODE RECONSTRUCTION")

    for py_file in INPUT_CODE_DIR.glob("*.py"):
        file_stem = py_file.stem

        # Must match Agent-3 naming EXACTLY
        agent3_json = AGENT3_DIR / f"{file_stem}.blocks_graph_agent3_full.json"

        if not agent3_json.exists():
            print(f" Skipping {file_stem}: no Agent-3 output")
            continue

        print(f"\n Processing {file_stem}.py")

        original_code = py_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        with agent3_json.open("r", encoding="utf-8") as f:
            agent3_result = json.load(f)

        try:
            fixed_code = generate_fixed_code(original_code, agent3_result)
        except Exception as e:
            print(f" Gemini error for {file_stem}: {e}")
            continue

        out_file = OUTPUT_DIR / f"{file_stem}.py"
        out_file.write_text(fixed_code, encoding="utf-8")

        print(f" Fixed code written → {out_file.name}")

    print("\n AGENT4 COMPLETE!")


if __name__ == "__main__":
    run_agent4()