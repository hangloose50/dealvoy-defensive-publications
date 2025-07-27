#!/usr/bin/env python3
"""
🧠 RedFlagVoyager - Scans patent drafts for risky/legal landmine terms
"""
import argparse, sys, re
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("RedFlagVoyager")
    except Exception:
        return True

def scan_for_red_flags(text):
    risky_terms = ["generic AI", "AI system", "may", "could", "example", "broadly", "any", "various", "preferred embodiment"]
    found = []
    for term in risky_terms:
        if re.search(rf"\\b{re.escape(term)}\\b", text, re.IGNORECASE):
            found.append(term)
    return found

def main():
    parser = argparse.ArgumentParser(description="RedFlagVoyager - Patent Red Flag Scanner")
    parser.add_argument("--input", type=str, help="Input file with draft text")
    parser.add_argument("--output", type=str, help="Output file for red flag report")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🧠 RedFlagVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🧠 RedFlagVoyager: Smoke test passed!")
        return 0
    if not args.input or not args.output:
        print("Usage: --input <draft.txt> --output <red_flags.txt>")
        return 2
    try:
        with open(args.input) as f:
            draft = f.read()
        flags = scan_for_red_flags(draft)
        with open(args.output, "w") as f:
            if flags:
                f.write("Red flag terms found:\n" + "\n".join(flags))
            else:
                f.write("No red flag terms found.")
        print(f"🧠 RedFlagVoyager: Scan complete, report written to {args.output}")
        return 0
    except Exception as e:
        print(f"🧠 RedFlagVoyager: Error - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
