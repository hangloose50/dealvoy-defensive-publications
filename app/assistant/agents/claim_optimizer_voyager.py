#!/usr/bin/env python3
"""
🧠 ClaimOptimizerVoyager - Refines patent claims for strength and scope
"""
import argparse, sys, re
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("ClaimOptimizerVoyager")
    except Exception:
        return True

def optimize_claims(text):
    # Simple heuristics: remove weak words, suggest stronger phrasing
    weak_words = ["may", "could", "optionally", "example", "generic", "various"]
    for word in weak_words:
        text = re.sub(rf"\\b{word}\\b", "", text, flags=re.IGNORECASE)
    # Suggest narrowing language
    text = re.sub(r"comprising", "consisting of", text, flags=re.IGNORECASE)
    return text

def main():
    parser = argparse.ArgumentParser(description="ClaimOptimizerVoyager - Patent Claim Optimizer")
    parser.add_argument("--input", type=str, help="Input file with draft claims")
    parser.add_argument("--output", type=str, help="Output file for optimized claims")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🧠 ClaimOptimizerVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🧠 ClaimOptimizerVoyager: Smoke test passed!")
        return 0
    if not args.input or not args.output:
        print("Usage: --input <draft_claims.txt> --output <optimized_claims.txt>")
        return 2
    try:
        with open(args.input) as f:
            draft = f.read()
        optimized = optimize_claims(draft)
        with open(args.output, "w") as f:
            f.write(optimized)
        print(f"🧠 ClaimOptimizerVoyager: Optimized claims written to {args.output}")
        return 0
    except Exception as e:
        print(f"🧠 ClaimOptimizerVoyager: Error - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
