from pathlib import Path  
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import os
import json
import ast
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from pathlib import Path
from typing import List, Dict, Any

# Optional Gemini
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False

MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# FIXED PROMPT: Escaped {{ }} braces for .format()
BLOCK_GRAPH_PROMPT = r"""
Think step by step internally.

Step 1: Identify block boundaries and types.
Step 2: Detect contains, control_flow, call, data_flow.
Step 3: Verify line ranges.
Step 4: Produce final JSON.

OUTPUT RULES:
- Return ONLY valid JSON.
- No explanation.
- No markdown.

FORMAT:
{{
  "nodes": [
    {{
      "id": "b1",
      "type": "function",
      "start_line": 1,
      "end_line": 8,
      "code": "def func(...):"
    }}
  ],
  "relationships": [
    {{"from": "b1", "to": "b2", "type": "contains"}}
  ]
}}

Code with line numbers:
{lines}
"""


# Enhanced AST Analyzer
class CodeBlockVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.relationships: List[Dict[str, Any]] = []
        self.block_id = 0
        self.current_function = None
        self.current_class = None
        self.prev_block = None
        self.source = None

    def _add_block(self, node, block_type: str):
        self.block_id += 1
        block_id = f"b{self.block_id}"
        end_line = getattr(node, 'end_lineno', node.lineno)
        self.nodes.append({
            "id": block_id,
            "type": block_type,
            "start_line": node.lineno,
            "end_line": end_line,
            "code": self._get_source(node)
        })
        
        # Add relationships
        if self.current_function or self.current_class:
            container = self.current_function or self.current_class
            self.relationships.append({"from": container, "to": block_id, "type": "contains"})
        if self.prev_block:
            self.relationships.append({"from": self.prev_block, "to": block_id, "type": "control_flow"})
        
        self.prev_block = block_id
        return block_id

    def visit_FunctionDef(self, node):
        block_id = self._add_block(node, "function")
        self.current_function = block_id
        self.generic_visit(node)
        self.current_function = None

    def visit_ClassDef(self, node):
        block_id = self._add_block(node, "class")
        self.current_class = block_id
        self.generic_visit(node)
        self.current_class = None

    def visit_Assign(self, node):
        self._add_block(node, "assignment")
        self.generic_visit(node)

    def visit_Return(self, node):
        self._add_block(node, "return")
        self.generic_visit(node)

    def visit_Call(self, node):
        self.block_id += 1
        block_id = f"b{self.block_id}"
        end_line = getattr(node, 'end_lineno', node.lineno)
        self.nodes.append({
            "id": block_id,
            "type": "call",
            "start_line": node.lineno,
            "end_line": end_line,
            "code": self._get_source(node)
        })
        if self.current_function or self.current_class:
            container = self.current_function or self.current_class
            self.relationships.append({"from": container, "to": block_id, "type": "contains"})
        if self.prev_block:
            self.relationships.append({"from": self.prev_block, "to": block_id, "type": "call"})
        self.prev_block = block_id
        self.generic_visit(node)

    def visit_If(self, node):
        self._add_block(node, "if")
        self.generic_visit(node)

    def visit_For(self, node):
        self._add_block(node, "for")
        self.generic_visit(node)

    def visit_While(self, node):
        self._add_block(node, "while")
        self.generic_visit(node)

    def visit_With(self, node):
        self._add_block(node, "with")
        self.generic_visit(node)

    def visit_Try(self, node):
        self._add_block(node, "try")
        self.generic_visit(node)

    def _get_source(self, node):
        try:
            if self.source:
                tree = ast.parse(self.source)
                return ast.get_source_segment(tree, node).strip()
        except:
            pass
        return f"{node.__class__.__name__}()"

def ast_analyze_code(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
        visitor = CodeBlockVisitor()
        visitor.source = code
        visitor.visit(tree)
        return {"nodes": visitor.nodes, "relationships": visitor.relationships}
    except SyntaxError:
        return {"nodes": [], "relationships": []}

# FIXED Gemini: Safe .format() + parsing
def analyze_with_gemini(code: str) -> Dict[str, Any]:
    if not HAS_GENAI or not GEMINI_API_KEY:
        return None
    
    numbered = "\n".join(f"{i+1}: {l}" for i, l in enumerate(code.splitlines()))
    prompt = BLOCK_GRAPH_PROMPT.format(lines=numbered)
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt, generation_config={"temperature": 0})
        
        # Robust parsing
        text = resp.text.strip().strip('```json').strip('```')
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            parsed = json.loads(text[start:end])
            if isinstance(parsed, dict) and 'nodes' in parsed:
                return parsed
        return None
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

def analyze_code(code: str) -> Dict[str, Any]:
    result = ast_analyze_code(code)
    if len(result["nodes"]) < 3:  # Gemini fallback
        gemini_result = analyze_with_gemini(code)
        if gemini_result:
            result = gemini_result
    return result

def build_graph_from_result(result: Dict[str, Any]) -> nx.DiGraph:
    G = nx.DiGraph()
    for node in result.get("nodes", []):
        start = node.get('start_line', '?')
        end = node.get('end_line', '?')  # Fixed: end_line, not end_lineno
        label = f"{start}-{end}: {node.get('type', 'unknown')}"
        G.add_node(node["id"], label=label, type=node.get("type", "unknown"))
    for rel in result.get("relationships", []):
        G.add_edge(rel["from"], rel["to"], label=rel["type"])
    return G


def get_python_files(root: Path) -> List[Path]:
    if root.is_file():
        return [root]
    files = []
    for ext in ("*.c", "*.txt"):
        files.extend(root.rglob(ext))
    return sorted(files)

def generate_block_graph(input_root: Path, out_root: Path) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    files = get_python_files(input_root)
    
    print(f"Scanning {input_root} ")
    if files:
        print(f"Found {len(files)} files")
    else:
        print(" No files - create ./input_path/*.c")
        return

    for f in files:
        print(f"\n {f.name}")
        code = f.read_text(encoding="utf-8", errors="ignore").strip()
        if not code:
            print("Empty - skip")
            continue

        result = analyze_code(code)
        G = build_graph_from_result(result)
        
        out_file = out_root / f"{f.stem}.blocks_graph.dot"
        write_dot(G, out_file.open("w"))
        print(f" {G.number_of_nodes()} nodes, {G.number_of_edges()} edges → {out_file.name}")

    print(f"\n Output: {out_root.absolute()}")

if __name__ == "__main__":
    INPUT_PATH = Path("./input_path/pandas_input_path_C")
    OUTPUT_PATH = Path("./agent1_results_cot/pandas_agent1_graph")
    generate_block_graph(INPUT_PATH, OUTPUT_PATH)