#!/usr/bin/env python3
"""Build Baseline table (55 programs, — for non-baseline libs) and COT_TOT table (100 programs)."""
import json
from pathlib import Path

BASE = Path(__file__).parent
RESULTS = BASE / "results"
C_COT = BASE / "COT_TOT_C" / "results_cot"
C_TOT = BASE / "COT_TOT_C" / "results_tot"
PY_COT = BASE / "COT_TOT_PYTHON" / "results_cot"
PY_TOT = BASE / "COT_TOT_PYTHON" / "results_tot"

BASELINE_LIBS = ["pandas", "fastapi", "mlib", "keras", "spacy"]
ALL_LIBS_ORDER = ["ansible", "black", "fastapi", "keras", "luigi", "mlib", "pandas", "scrapy", "spacy", "tornado"]

def load_json(p):
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    # Baseline: from results/ (only 5 libs)
    baseline = {}
    for lib in BASELINE_LIBS:
        j = load_json(RESULTS / f"{lib}_agent4_similarity_results.json")
        for prog, v in j.items():
            baseline[(lib, prog)] = (v["levenshtein_distance"], v["cosine_similarity"])

    # COT_TOT_C and COT_TOT_PYTHON: both COT and TOT
    c_tot = {}
    c_cot = {}
    py_tot = {}
    py_cot = {}
    for lib in ALL_LIBS_ORDER:
        jc_tot = load_json(C_TOT / f"{lib}_agent4_similarity_results.json")
        jc_cot = load_json(C_COT / f"{lib}_agent4_similarity_results.json")
        jp_tot = load_json(PY_TOT / f"{lib}_agent4_similarity_results.json")
        jp_cot = load_json(PY_COT / f"{lib}_agent4_similarity_results.json")
        for k, v in jc_tot.items():
            c_tot[(lib, k)] = (v["levenshtein_distance"], v["cosine_similarity"])
        for k, v in jc_cot.items():
            c_cot[(lib, k)] = (v["levenshtein_distance"], v["cosine_similarity"])
        for k, v in jp_tot.items():
            py_tot[(lib, k)] = (v["levenshtein_distance"], v["cosine_similarity"])
        for k, v in jp_cot.items():
            py_cot[(lib, k)] = (v["levenshtein_distance"], v["cosine_similarity"])

    # Canonical list of (lib, program) for 100 programs from C_TOT
    rows_100 = []
    for lib in ALL_LIBS_ORDER:
        j = load_json(C_TOT / f"{lib}_agent4_similarity_results.json")
        for prog in sorted(j.keys(), key=lambda x: (len(x), x)):
            stem = prog.replace(".c", "").replace(".py", "")
            rows_100.append((lib, prog, stem))

    # Build Table 1: Baseline (100 rows; — for non-baseline libs)
    lines1 = []
    lines1.append("# Table 1: Baseline (results/) — 5 libraries, 55 programs with metrics; — for ansible, black, luigi, scrapy, tornado")
    lines1.append("")
    lines1.append("| # | Library | Program | Baseline Levenshtein | Baseline Cosine |")
    lines1.append("|---|---------|---------|----------------------|-----------------|")
    for i, (lib, prog, stem) in enumerate(rows_100, 1):
        py_name = stem + ".py"
        if lib in BASELINE_LIBS and (lib, py_name) in baseline:
            lev, cos = baseline[(lib, py_name)]
            lines1.append(f"| {i} | {lib} | {py_name} | {lev} | {cos:.4f} |")
        else:
            lines1.append(f"| {i} | {lib} | {py_name} | — | — |")

    # Build Table 2: COT_TOT_C and COT_TOT_PYTHON (100 programs)
    lines2 = []
    lines2.append("# Table 2: COT_TOT_C and COT_TOT_PYTHON — 10 libraries, 100 programs")
    lines2.append("")
    lines2.append("| # | Library | Program | COT_TOT_C Lev | COT_TOT_C Cos | COT_TOT_PYTHON Lev | COT_TOT_PYTHON Cos |")
    lines2.append("|---|---------|---------|----------------|----------------|---------------------|---------------------|")
    for i, (lib, prog, stem) in enumerate(rows_100, 1):
        c_key = (lib, prog)
        py_key = (lib, stem + ".py")
        lev_c, cos_c = c_tot.get(c_key, (None, None))
        lev_p, cos_p = py_tot.get(py_key, (None, None))
        s_lev_c = str(lev_c) if lev_c is not None else "—"
        s_cos_c = f"{cos_c:.4f}" if cos_c is not None else "—"
        s_lev_p = str(lev_p) if lev_p is not None else "—"
        s_cos_p = f"{cos_p:.4f}" if cos_p is not None else "—"
        lines2.append(f"| {i} | {lib} | {stem} | {s_lev_c} | {s_cos_c} | {s_lev_p} | {s_cos_p} |")

    # Table 3: C — graph_based = TOT, english = COT
    lines3 = []
    lines3.append("# Table 3: C — graph_based_LD, english_cot_tot, graph_based_cos_sim, english_tot_cot")
    lines3.append("")
    lines3.append("(graph_based = TOT, english = COT from COT_TOT_C.)")
    lines3.append("")
    lines3.append("| # | Library | Program | graph_based_LD | english_cot_tot | graph_based_cos_sim | english_tot_cot |")
    lines3.append("|---|---------|---------|-----------------|-----------------|---------------------|-----------------|")
    for i, (lib, prog, stem) in enumerate(rows_100, 1):
        c_key = (lib, prog)
        lev_tot, cos_tot = c_tot.get(c_key, (None, None))
        lev_cot, cos_cot = c_cot.get(c_key, (None, None))
        a = str(lev_tot) if lev_tot is not None else "—"
        b = str(lev_cot) if lev_cot is not None else "—"
        c = f"{cos_tot:.4f}" if cos_tot is not None else "—"
        d = f"{cos_cot:.4f}" if cos_cot is not None else "—"
        lines3.append(f"| {i} | {lib} | {stem} | {a} | {b} | {c} | {d} |")

    # Table 4: Python — graph_based = baseline (results/), english_cot_tot = COT, english_tot_cot = TOT
    lines4 = []
    lines4.append("# Table 4: Python — graph_based_LD, english_cot_tot, graph_based_cos_sim, english_tot_cot")
    lines4.append("")
    lines4.append("(graph_based = baseline from results/; english_cot_tot = COT, english_tot_cot = TOT from COT_TOT_PYTHON.)")
    lines4.append("")
    lines4.append("| # | Library | Program | graph_based_LD | english_cot_tot | graph_based_cos_sim | english_tot_cot |")
    lines4.append("|---|---------|---------|-----------------|-----------------|---------------------|-----------------|")
    for i, (lib, prog, stem) in enumerate(rows_100, 1):
        py_name = stem + ".py"
        lev_base, cos_base = baseline.get((lib, py_name), (None, None))
        lev_cot, cos_cot = py_cot.get((lib, py_name), (None, None))
        lev_tot, cos_tot = py_tot.get((lib, py_name), (None, None))
        a = str(lev_base) if lev_base is not None else "—"
        b = str(lev_cot) if lev_cot is not None else "—"
        c = f"{cos_base:.4f}" if cos_base is not None else "—"
        d = f"{cos_tot:.4f}" if cos_tot is not None else "—"
        lines4.append(f"| {i} | {lib} | {py_name} | {a} | {b} | {c} | {d} |")

    out = BASE / "results" / "RESULTS_TABLE.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines1))
        f.write("\n\n---\n\n")
        f.write("\n".join(lines2))
        f.write("\n\n---\n\n")
        f.write("\n".join(lines3))
        f.write("\n\n---\n\n")
        f.write("\n".join(lines4))
    print(f"Wrote {out}")
    print(f"Table 1–2 rows: {len(rows_100)}; Table 3 (C) and Table 4 (Python) added.")

if __name__ == "__main__":
    main()
