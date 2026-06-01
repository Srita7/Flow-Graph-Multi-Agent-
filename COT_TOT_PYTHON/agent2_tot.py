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
RELATION-FIRST SEMANTIC FAULT DETECTOR
Tree-of-Thought Reasoning Enabled

You are a deterministic static analyzer.

You MUST use multi-path reasoning internally.
DO NOT output reasoning.
OUTPUT JSON ONLY.

=================================================
PHASE 1 — BUILD COMPLETE RELATION MAP

For each node:
- List all incoming edges grouped by type
- List all outgoing edges grouped by type
- Identify root reachability
- Identify containment hierarchy depth

=================================================
PHASE 2 — GENERATE MULTIPLE FAULT HYPOTHESES

For each node, internally generate possible violation hypotheses
based on:

contains violations:
- illegal parent type
- hierarchy cycle

data_flow violations:
- assignment without consumer
- return without producer
- missing data convergence

control_flow violations:
- inconsistent sequence
- unreachable node
- assignment chains without branching

call violations:
- call outside function containment
- unreachable call

Generate multiple possible interpretations per node.

=================================================
PHASE 3 — EVALUATE & SCORE HYPOTHESES

For each hypothesis:
- Check strict rule consistency
- Validate graph evidence
- Eliminate weak hypotheses
- Select strongest valid violation

Each node may match AT MOST ONE fault pattern.

If none valid → node is clean.

=================================================
PHASE 4 — GLOBAL CONSISTENCY CHECK

Ensure:
- No contradictory classifications
- No duplicate fault types per node
- Summary counts match faulty_nodes length

=================================================
FAULT PATTERNS (Choose EXACTLY ONE if violated)

BROKEN_DEPENDENCY  
FLOW_MISMATCH  
INCOMPLETE_CONVERGENCE  
ORPHANED_COMPUTATION  
CIRCULAR_DEPENDENCY  
DISCONNECTED_RETURN  
UNREACHABLE_CALL  

=================================================
FAULT SCORE
0 = clean  
10 = definitely broken  

=================================================
CRITICAL OUTPUT RULES
- JSON ONLY
- No explanation text
- No markdown
- If no defects → faulty_nodes must be []

=================================================
GRAPH STRUCTURE
Total Nodes: {total_nodes}
Edge Types: {edge_types}
Root Node: {root_node}
Avg Degree: {avg_degree:.1f}

DOT Content Preview:
{nodes_preview}

Relations Sample:
{relations_sample}

=================================================
STRICT JSON FORMAT

{{
  "file_name": "{file_stem}",
  "total_nodes": {total_nodes},
  "avg_degree": {avg_degree:.1f},
  "faulty_nodes": [
    {{
      "node_id": "b4",
      "type": "assignment",
      "relations_in": ["b1(contains)"],
      "relations_out": [],
      "fault_score": 8,
      "fault_type": "BROKEN_DEPENDENCY"
    }}
  ],
  "fault_summary": {{
    "total_faults": 0,
    "common_patterns": [],
    "clean_nodes": 0
  }}
}}
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
    INPUT_FOLDER = Path("./agent1_results_tot/tornado_agent1_graph")
    OUTPUT_FOLDER = Path("./agent2_results_tot/tornado_agent2_results")
    batch_analyze_folder(INPUT_FOLDER, OUTPUT_FOLDER)
