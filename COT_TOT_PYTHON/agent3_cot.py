from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import os
import json
import networkx as nx
from networkx.drawing.nx_pydot import read_dot, to_pydot
from typing import Dict, Any, List
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

# COMPLETE AGENT3_PROMPT (your exact version)
AGENT3_PROMPT = r"""
GRAPH SURGICAL REPAIR AGENT – DETERMINISTIC MODE

You are Agent-3.

Agent-1 built the graph.
Agent-2 diagnosed the faults.

Your mission:
repair structural dependency errors with the SMALLEST legal modification
and then output the COMPLETE corrected graph.

You NEVER generate source code.

Think internally step-by-step, but OUTPUT JSON ONLY.

--------------------------------------------------

INPUT
File: {file_name}
Fault Count: {total_faults}

Faulty Nodes:
{faulty_nodes_details}

Graph Info:
Total Nodes: {total_nodes}
Root Node: {root_node}

Original Graph:
{full_graph_dot}

--------------------------------------------------

FOR EACH FAULTY NODE FOLLOW EXACTLY THIS PROCESS

STEP 1 — INSPECT  
List its incoming and outgoing relations.
Identify missing producer / consumer / hierarchy.

STEP 2 — DIAGNOSE  
Explain why the current structure violates the fault_type.

STEP 3 — PROPOSE MINIMAL PATCH  
Prefer in this order:
1. add one edge  
2. change label  
3. add one tiny temp node (ONLY for cycles)

STEP 4 — VERIFY  
After patch:
✓ node becomes valid  
✓ no new cycles unless required  
✓ other nodes unaffected  
✓ graph remains connected  

STEP 5 — APPLY  
Integrate ONLY this patch into the original graph.

--------------------------------------------------

REPAIR RULES (STRICT)

BROKEN_DEPENDENCY  
→ add data_flow producer → consumer.

FLOW_MISMATCH  
→ replace control_flow with data_flow.

INCOMPLETE_CONVERGENCE  
→ add missing data_flow into return.

ORPHANED_COMPUTATION  
→ connect to nearest downstream usage.

CIRCULAR_DEPENDENCY  
→ break via one intermediate node.

DISCONNECTED_RETURN  
→ connect nearest assignment.

UNREACHABLE_CALL  
→ add contains from function.

--------------------------------------------------

GLOBAL HARD CONSTRAINTS

MINIMALITY FIRST.

You must:
✓ keep ALL original nodes  
✓ keep ALL correct edges  
✓ add/change only what is required  
✓ output full valid DOT  

Never:
✗ rename  
✗ delete  
✗ redesign  
✗ optimize  
✗ refactor  

--------------------------------------------------

OUTPUT RULES

JSON ONLY 
No explanations 
No markdown 

rectified_nodes should contain ONLY nodes actually modified.

--------------------------------------------------

STRICT JSON FORMAT

{{
  "file_name": "{file_stem}",
  "rectified_nodes": [
    {{
      "node_id": "b4",
      "fault_type": "BROKEN_DEPENDENCY",
      "fix_description": "Added data_flow b2→b4",
      "confidence": 9
    }}
  ],
  "full_rectified_graph": "digraph G {{ ... COMPLETE GRAPH ... }}",
  "rectification_summary": {{
    "total_fixes": 0,
    "edge_additions": 0,
    "edge_modifications": 0,
    "nodes_added": 0
  }}
}}
"""



class FullGraphRepairAgent:
    """AGENT3: PRODUCTION-READY full graph repair - ALL BUGS FIXED."""

    def __init__(self):
        pass

    def get_full_graph_dot(self, G: nx.DiGraph) -> str:
        """ FIXED: Generate CLEAN valid DOT - no double digraph."""
        try:
            pydot_graph = to_pydot(G)
            dot_str = str(pydot_graph).strip()
            
            # CRITICAL: Remove malformed nested structures
            dot_str = re.sub(r'strict digraph\s*\{', '{', dot_str, flags=re.MULTILINE)
            dot_str = re.sub(r'^digraph G\s*\{', 'digraph G {', dot_str, flags=re.MULTILINE)
            
            # Ensure proper single digraph wrapper
            if not dot_str.startswith('digraph G {'):
                dot_str = 'digraph G {\n' + dot_str.lstrip('digraph G {') + '\n}'
            
            # Clean extra braces and whitespace
            dot_str = re.sub(r'\{\s*\}', '{}', dot_str)
            dot_str = re.sub(r'\}\s*\}\s*$', '}', dot_str, flags=re.MULTILINE)
            dot_str = re.sub(r'\n\s*\n', '\n', dot_str)  # Clean empty lines
            
            return dot_str.strip()
            
        except Exception:
            # BULLETPROOF MANUAL DOT GENERATION
            lines = ['digraph G {']
            
            # Nodes with proper escaping
            for node, data in G.nodes(data=True):
                label = str(data.get('label', node))
                label = label.replace('"', '\\"').replace('\n', '\\n')
                node_type = data.get('type', '')
                lines.append(f'  "{node}" [label="{label}", type="{node_type}"];')
            
            # Edges with proper escaping
            for u, v, data in G.edges(data=True):
                label = str(data.get('label', ''))
                label = label.replace('"', '\\"')
                color = data.get('color', 'black')
                lines.append(f'  "{u}" -> "{v}" [label="{label}", color="{color}"];')
            
            lines.append('}')
            return '\n'.join(lines)

    def get_root_node(self, G: nx.DiGraph) -> str:
        """ FIXED: Proper root detection."""
        # Find nodes with highest 'contains' out-degree
        contains_degree = {}
        for u, v, data in G.edges(data=True):
            if data.get('label') == 'contains':
                contains_degree[u] = contains_degree.get(u, 0) + 1
        
        if contains_degree:
            return max(contains_degree, key=contains_degree.get)
        return "none"

    def prepare_repair_data(self, agent2_result: Dict[str, Any], G: nx.DiGraph) -> Dict[str, Any]:
        """Prepare complete repair context."""
        file_stem = agent2_result["file_name"]
        
        # Fault details with relations
        faulty_details = []
        for node_data in agent2_result.get("faulty_nodes", []):
            node_id = node_data['node_id']
            fault_type = node_data['fault_type']
            node_type = node_data.get('type', '?')
            in_rel = ', '.join(node_data.get('relations_in', ['none']))
            out_rel = ', '.join(node_data.get('relations_out', ['none']))
            detail = f"- {node_id} ({node_type}): {fault_type} | in: [{in_rel}] | out: [{out_rel}]"
            faulty_details.append(detail)
        
        total_faults = len(agent2_result.get("faulty_nodes", []))
        total_nodes = len(G.nodes)
        root_node = self.get_root_node(G)
        full_dot = self.get_full_graph_dot(G)
        
        return {
            "file_name": file_stem,
            "file_stem": file_stem,
            "total_faults": total_faults,
            "faulty_nodes_details": '\n'.join(faulty_details),
            "total_nodes": total_nodes,
            "root_node": root_node,
            "full_graph_dot": full_dot
        }

    def repair_complete_graph(self, agent2_json_path: Path, dot_path: Path) -> Dict[str, Any]:
        """Main repair execution."""
        file_stem = agent2_json_path.stem.replace('_agent2', '')
        print(f"\n Repairing {file_stem}")
        
        # Load diagnosis
        try:
            with agent2_json_path.open('r', encoding='utf-8') as f:
                agent2_result = json.load(f)
        except Exception as e:
            print(f" Load diagnosis: {e}")
            return {"rectified_nodes": []}
        
        # Load patient graph
        try:
            G = nx.DiGraph(read_dot(str(dot_path)))
            print(f" {len(G.nodes)} nodes | {len(G.edges)} edges")
        except Exception as e:
            print(f" Load graph: {e}")
            return {"rectified_nodes": []}
        
        # Surgical preparation
        repair_data = self.prepare_repair_data(agent2_result, G)
        prompt = AGENT3_PROMPT.format(**repair_data)
        
        # Execute repair
        result = self._llm_full_repair(prompt, file_stem)
        return result

    def _llm_full_repair(self, prompt: str, file_stem: str) -> Dict[str, Any]:
        """Gemini surgical repair."""
        if not HAS_GENAI or not GEMINI_API_KEY:
            print(" No Gemini available")
            return {"rectified_nodes": []}
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(MODEL_NAME)
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.0,
                    "response_mime_type": "application/json",
                    "max_output_tokens": 25000
                }
            )
            
            text = response.text.strip()
            result = self._extract_full_json(text)
            
            if result and result.get('full_rectified_graph', '').strip():
                fixes = len(result.get('rectified_nodes', []))
                print(f" {fixes} repairs | Graph ready")
                return result
            else:
                print(" No repaired graph")
                self._debug_repair(prompt, text, file_stem)
                return {"rectified_nodes": []}
        except Exception as e:
            print(f" Repair error: {e}")
            return {"rectified_nodes": []}

    def _extract_full_json(self, text: str) -> Dict[str, Any]:
        """Industrial JSON extraction."""
        # Strip markdown
        cleaned = re.sub(r'```(?:json)?\s*|\s*```\s*$', '', text, flags=re.DOTALL).strip()
        
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict) and 'full_rectified_graph' in parsed:
                return parsed
        except:
            pass
        
        # Find complete JSON block
        brace_count = 0
        start_idx = -1
        for i, char in enumerate(text):
            if char == '{':
                if brace_count == 0:
                    start_idx = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_idx >= 0:
                    try:
                        candidate = text[start_idx:i+1]
                        parsed = json.loads(candidate)
                        if 'full_rectified_graph' in parsed:
                            return parsed
                    except:
                        pass
                    start_idx = -1
        
        return None

    def _debug_repair(self, prompt: str, response: str, file_stem: str):
        """Debug export."""
        debug_file = f"debug_{file_stem}.txt"
        with open(debug_file, "w", encoding='utf-8') as f:
            f.write(f"PROMPT ({len(prompt)} chars):\n{prompt[:4000]}\n\n")
            f.write(f"RESPONSE:\n{response}")
        print(f" Debug: {debug_file}")

def batch_full_repair(agent2_folder: Path, graphs_folder: Path, output_folder: Path) -> None:
    """Production batch repair."""
    output_folder.mkdir(parents=True, exist_ok=True)
    
    print(" AGENT3 FULL REPAIR ACTIVATED")
    agent2_files = sorted(agent2_folder.glob("*_agent2.json"))
    
    print(f" {len(agent2_files)} graphs queued")
    
    total_fixes = 0
    for json_file in agent2_files:
        file_stem = json_file.stem.replace('_agent2', '')
        dot_file = graphs_folder / f"{file_stem}.dot"
        
        if not dot_file.exists():
            print(f"  Missing: {dot_file}")
            continue
        
        result = FullGraphRepairAgent().repair_complete_graph(json_file, dot_file)
        
        # Save repair package
        pkg_file = output_folder / f"{file_stem}_agent3_full.json"
        with pkg_file.open("w", encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        # Extract repaired graph
        if 'full_rectified_graph' in result:
            repaired_dot = output_folder / f"{file_stem}_repaired.dot"
            with repaired_dot.open("w", encoding='utf-8') as f:
                f.write(result['full_rectified_graph'])
            print(f"   {file_stem:<15}  {len(result['rectified_nodes'])} fixes")
        else:
            print(f"   {file_stem:<15}   No repair")
        
        total_fixes += len(result.get('rectified_nodes', []))
    
    print(f"\n PIPELINE COMPLETE | {total_fixes} total fixes")

if __name__ == "__main__":
    AGENT2_FOLDER = Path("./agent2_results_cot/tornado_agent2_results")
    GRAPHS_FOLDER = Path("./agent1_results_cot/tornado_agent1_graph")
    OUTPUT_FOLDER = Path("./agent3_results_cot/tornado_agent3_rectified_graph")
    
    batch_full_repair(AGENT2_FOLDER, GRAPHS_FOLDER, OUTPUT_FOLDER)


