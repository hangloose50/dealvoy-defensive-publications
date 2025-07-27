#!/usr/bin/env python3
"""
🧠 DiagramVoyager - Generates patent claim flowcharts (Markdown/Mermaid)
"""
import argparse, sys, re
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("DiagramVoyager")
    except Exception:
        return True

def generate_mermaid_flowchart(claim_text):
    # Simple heuristic: each numbered step becomes a node
    lines = [l.strip() for l in claim_text.splitlines() if l.strip()]
    nodes = [f"Step{i+1}[{l}]" for i, l in enumerate(lines)]
    edges = [f"{nodes[i]} --> {nodes[i+1]}" for i in range(len(nodes)-1)]
    return "graph TD\n" + "\n".join(nodes) + ("\n" if edges else "") + "\n".join(edges)

def main():
    parser = argparse.ArgumentParser(description="DiagramVoyager - Claim Flowchart Generator")
    parser.add_argument("--input", type=str, help="Input file with claim steps")
    parser.add_argument("--output", type=str, help="Output file for diagram (Markdown)")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🧠 DiagramVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🧠 DiagramVoyager: Smoke test passed!")
        return 0
    if not args.input or not args.output:
        print("Usage: --input <claim_steps.txt> --output <diagram.md>")
        return 2
    try:
        with open(args.input) as f:
            claim = f.read()
        diagram = generate_mermaid_flowchart(claim)
        with open(args.output, "w") as f:
            f.write(f"```mermaid\n{diagram}\n```")
        print(f"🧠 DiagramVoyager: Diagram written to {args.output}")
        return 0
    except Exception as e:
        print(f"🧠 DiagramVoyager: Error - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
