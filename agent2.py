from pathlib import Path  
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)  

import os
import json
import networkx as nx
from networkx.drawing.nx_pydot import read_dot
from typing import List, Dict, Any
from collections import Counter, deque
import re


# Optional Gemini
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

# YOUR PROMPT (exact)
AGENT2_PROMPT = r"""
SEMANTIC CODE GRAPH ANALYZER - RELATION-DRIVEN FAULT DETECTION

=== GRAPH STRUCTURE ===
Total Nodes: {total_nodes} | Edge Types: {edge_types}
Root Node: {root_node} | Avg Degree: {avg_degree:.1f}

=== RELATIONSHIP ANALYSIS (Primary) ===
Analyze ALL edge types FIRST:
- contains: Hierarchical (function→assignment OK, cycles BAD)
- data_flow: Dependency (assignment→return REQUIRED)  
- control_flow: Branching (if→assignment OK, assignment→assignment BAD)
- call: Invocation (function→call→return expected)

=== SEMANTIC PATTERNS TO DETECT (NO self-loops/density bias) ===

1. **BROKEN DEPENDENCY**: assignment → NO data_flow → return/call
2. **FLOW MISMATCH**: control_flow between data-dependent blocks (assignment→assignment)
3. **INCOMPLETE CONVERGENCE**: Multiple assignment → single return (missing paths)
4. **ORPHANED COMPUTATION**: assignment → NO downstream data_flow
5. **CIRCULAR DEPENDENCY**: data_flow cycles (assignment→assignment→assignment)
6. **DISCONNECTED RETURN**: return → NO incoming data_flow from function scope
7. **UNREACHABLE CALL**: call → NO path from function contains

=== YOUR JOB ===
1. Map ALL relations for each node
2. Score SEMANTIC correctness (0-10)
3. Flag ONLY true defects (0 if clean)

=== GRAPH DATA ===
DOT Content Preview:
{nodes_preview}
Relations Sample: {relations_sample}

JSON FORMAT (STRICT):
{{
  "file_name": "{file_stem}",
  "total_nodes": {total_nodes},
  "avg_degree": {avg_degree:.1f},
  "faulty_nodes": [
    {{
      "node_id": "b4",
      "type": "function",
      "relations_in": ["bX(data_flow)"],
      "relations_out": ["contains→b5", "data_flow→b7"], 
      "fault_score": 8,
      "fault_type": "incomplete_convergence"
    }}
  ],
  "fault_summary": {{
    "total_faults": 1,
    "common_patterns": ["incomplete_convergence"],
    "clean_nodes": 15
  }}
}}

CRITICAL: 
- NO self-loop/density judgments
- Relations → Semantic → Fault (3 steps)  
- Empty faulty_nodes[] if NO defects
- Concrete relation paths in reasoning
RESPOND JSON ONLY.
"""


class FaultyNodeDetector:
    """Full Agent2 - FULLY FIXED: JSON extraction + debugging."""
    
    def __init__(self):
        pass
    
    def prepare_graph_data(self, G: nx.DiGraph, file_stem: str) -> Dict[str, Any]:
        """Extract prompt variables."""
        total_nodes = len(G.nodes)
        avg_degree = sum(dict(G.degree()).values()) / total_nodes if total_nodes else 0
        
        # Edge types
        edge_types = Counter()
        for u, v, data in G.edges(data=True):
            label = data.get('label', 'unknown')
            edge_types[label] += 1
        edge_types_str = "; ".join(f"{k}:{v}" for k,v in edge_types.most_common())
        
        # Root (highest contains out-degree)
        contains_degree = Counter()
        for u, v, data in G.edges(data=True):
            if data.get('label') == 'contains':
                contains_degree[u] += 1
        root_node = max(contains_degree, key=contains_degree.get, default="none")
        
        # Nodes preview (first 6)
        nodes_preview = "\n".join([
            f"{n}: {G.nodes[n].get('label', n)} ({G.nodes[n].get('type', '?')})"
            for n in list(G.nodes)[:6]
        ])
        
        # Relations sample (first 8 edges)
        relations_sample = []
        for u, v, data in list(G.edges(data=True))[:8]:
            relations_sample.append(f"{u}[{data.get('label', '?')}]→{v}")
        relations_sample_str = "\n".join(relations_sample)
        
        return {
            "total_nodes": total_nodes,
            "edge_types": edge_types_str,
            "root_node": root_node,
            "avg_degree": avg_degree,
            "nodes_preview": nodes_preview,
            "relations_sample": relations_sample_str,
            "file_stem": file_stem
        }
    
    def analyze_graph(self, dot_path: Path) -> Dict[str, Any]:
        """Complete analysis."""
        try:
            G = nx.DiGraph(read_dot(str(dot_path)))
        except Exception as e:
            print(f" Failed to read DOT {dot_path}: {e}")
            return {"faulty_nodes": []}
            
        file_stem = dot_path.stem
        
        prompt_data = self.prepare_graph_data(G, file_stem)
        prompt = AGENT2_PROMPT.format(**prompt_data)
        
        result = self._llm_analysis(prompt, file_stem)
        
        # Ensure valid structure
        if not isinstance(result, dict) or 'faulty_nodes' not in result:
            print(f"  {file_stem}: Invalid structure - using fallback")
            result = {
                "file_name": file_stem,
                "total_nodes": len(G.nodes),
                "avg_degree": 0.0,
                "faulty_nodes": [],
                "fault_summary": {"total_faults": 0, "clean_nodes": len(G.nodes)}
            }
        
        return result
    
    def _llm_analysis(self, prompt: str, file_stem: str) -> Dict[str, Any]:
        """FIXED: Bulletproof LLM call + JSON extraction."""
        if not HAS_GENAI or not GEMINI_API_KEY:
            print(f" {file_stem}: No Gemini available")
            return {"faulty_nodes": []}
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(
                prompt, 
                generation_config={"temperature": 0.0, "response_mime_type": "application/json"}
            )
            
            text = response.text.strip()
            print(f" {file_stem}: Response ({len(text)} chars): {text[:150]}...")
            
            result = self._extract_json(text)
            
            if result:
                faults_count = len(result.get('faulty_nodes', []))
                print(f" {file_stem}: Found {faults_count} faults")
                return result
            else:
                print(f" {file_stem}: JSON extraction failed - saving response")
                with open(f"debug_response_{file_stem}.txt", "w") as f:
                    f.write(f"PROMPT:\n{prompt}\n\nRESPONSE:\n{text}")
                return {"faulty_nodes": []}
                
        except Exception as e:
            print(f" {file_stem}: LLM error: {str(e)[:100]}")
            return {"faulty_nodes": []}
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """FIXED: Industrial-strength JSON extraction."""
        
        # Strategy 1: Try direct json.loads on cleaned text
        cleaned = re.sub(r'```(?:json)?\s*', '', text, flags=re.DOTALL)
        cleaned = re.sub(r'\s*```\s*$', '', cleaned, flags=re.DOTALL)
        cleaned = cleaned.strip()
        
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict) and 'faulty_nodes' in parsed:
                return parsed
        except:
            pass
        
        # Strategy 2: Find balanced JSON blocks
        def find_json_blocks(text):
            stack = []
            candidates = []
            i = 0
            while i < len(text):
                if text[i] == '{':
                    start = i
                    stack.append(i)
                    i += 1
                    while stack and i < len(text):
                        if text[i] == '{':
                            stack.append(i)
                        elif text[i] == '}':
                            stack.pop()
                        i += 1
                    if not stack and start < i:
                        candidates.append((start, i))
                else:
                    i += 1
            
            # Test largest first
            candidates.sort(key=lambda x: x[1]-x[0], reverse=True)
            for start, end in candidates[:3]:
                try:
                    candidate = text[start:end]
                    parsed = json.loads(candidate)
                    if isinstance(parsed, dict) and 'faulty_nodes' in parsed:
                        return parsed
                except:
                    continue
            return None
        
        result = find_json_blocks(text)
        if result:
            return result
        
        # Strategy 3: Regex fallback (improved)
        patterns = [
            r'\{[^{}]*?(?:\{[^{}]*?\}[^{}]*?)*\}',
            r'\{.*\}',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group())
                    if isinstance(parsed, dict) and 'faulty_nodes' in parsed:
                        return parsed
                except:
                    continue
        
        return None


def batch_analyze_folder(input_folder: Path, output_folder: Path) -> None:
    """Batch processing."""
    output_folder.mkdir(parents=True, exist_ok=True)
    detector = FaultyNodeDetector()
    
    print(" AGENT2: Semantic Code Graph Analysis Starting...")
    dot_files = list(input_folder.glob("*.dot"))
    
    if not dot_files:
        print(" No .dot files found!")
        return
    
    print(f" Found {len(dot_files)} graph files")
    
    total_faults = 0
    for dot_file in dot_files:
        print(f"\n Processing {dot_file.name}...")
        result = detector.analyze_graph(dot_file)
        
        out_file = output_folder / f"{dot_file.stem}_agent2.json"
        with out_file.open("w") as f:
            json.dump(result, f, indent=2)
        
        faults = len(result.get("faulty_nodes", []))
        total_faults += faults
        print(f"   → {faults} faults detected | {result.get('fault_summary', {}).get('clean_nodes', 0)} clean nodes")
    
    print(f"\n COMPLETE! Total faults across {len(dot_files)} files: {total_faults}")
    #print(f" Results saved to: {output_folder.absolute()}")


if __name__ == "__main__":
    INPUT_FOLDER = Path("./agent1_graph/pandas_agent1_graph")
    OUTPUT_FOLDER = Path("./agent2_results/pandas_agent2_results")
    batch_analyze_folder(INPUT_FOLDER, OUTPUT_FOLDER)
