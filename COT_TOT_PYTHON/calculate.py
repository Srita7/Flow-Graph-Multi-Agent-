from pathlib import Path
import math
import json
from collections import Counter


# -------- PATH CONFIG --------
INPUT_DIR = Path("./input_path/tornado_input_path")
OUTPUT_DIR = Path("./agent4_results_cot/tornado_agent4_output_code")

# FIXED: Create 'results' folder if missing
RESULTS_DIR = Path("./results_cot")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULT_FILE = RESULTS_DIR / "tornado_agent4_similarity_results.json"
# -----------------------------


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------- LEVENSHTEIN DISTANCE ----------------
def levenshtein_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))

    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insert = current[j - 1] + 1
            delete = previous[j] + 1
            replace = previous[j - 1] + (ca != cb)
            current.append(min(insert, delete, replace))
        previous = current

    return previous[-1]


# ---------------- LINE-LEVEL EDIT DISTANCE ----------------
def line_edit_distance(a: str, b: str) -> int:
    a_lines = a.splitlines()
    b_lines = b.splitlines()

    diff = sum(x != y for x, y in zip(a_lines, b_lines))
    diff += abs(len(a_lines) - len(b_lines))

    return diff


# ---------------- COSINE SIMILARITY ----------------
def cosine_similarity(a: str, b: str) -> float:
    def char_ngrams(text, n=3):
        return [text[i:i+n] for i in range(len(text) - n + 1)]

    vec1 = Counter(char_ngrams(a))
    vec2 = Counter(char_ngrams(b))

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)

    denominator = math.sqrt(sum(v*v for v in vec1.values())) * \
                  math.sqrt(sum(v*v for v in vec2.values()))

    if not denominator:
        return 0.0

    return numerator / denominator


# ---------------- MAIN ----------------
def main():
    results = {}

    # Process all input files
    for input_file in INPUT_DIR.glob("*.py"):
        output_file = OUTPUT_DIR / input_file.name

        if not output_file.exists():
            print(f"Missing output: {output_file}")
            continue

        print(f"Comparing {input_file.name}")

        original = read_file(input_file)
        fixed = read_file(output_file)

        results[input_file.name] = {
            "levenshtein_distance": levenshtein_distance(original, fixed),
            "cosine_similarity": round(cosine_similarity(original, fixed), 4),
            "line_edit_distance": line_edit_distance(original, fixed)
        }

    # FIXED: Directory now guaranteed to exist
    with RESULT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f" Results saved: {RESULT_FILE}")
   # print("Sample:", list(results.keys())[:3])


if __name__ == "__main__":
    main()
