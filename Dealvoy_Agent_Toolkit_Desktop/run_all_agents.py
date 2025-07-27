#!/usr/bin/env python3
"""
Run all Dealvoy AI agents and generate intelligence reports for desktop use.
"""
import sys
import os
from pathlib import Path

# Add ai_systems directory to path
ai_systems_path = Path(__file__).parent.parent / "app" / "ai_systems"
sys.path.insert(0, str(ai_systems_path))

AGENT_CLASSES = [
    "DealvoyModelVoyager",
    "DealvoyCategoryAI",
    "DealvoyTrendAI",
    "DealvoySupplierMatch",
    "DealvoyLabelGenerator",
    "DealExplainerAI",
    "ProductClusterAI",
    "RiskForecasterAI",
    "CashflowPredictorAI",
    # Add additional agent classes here as implemented
]

AGENT_MODULES = [
    "dealvoymodelvoyager",
    "dealvoycategoryai",
    "dealvoytrendai",
    "dealvoysuppliermatch",
    "dealvoylabelgenerator",
    "dealexplainerai",
    "productclusterai",
    "riskforecasterai",
    "cashflowpredictorai",
    # Add additional agent modules here as implemented
]

def run_all_agents():
    print("\n🖥️ Running All Dealvoy AI Agents (Desktop Toolkit)")
    print("=" * 60)
    results = {}
    for module_name, class_name in zip(AGENT_MODULES, AGENT_CLASSES):
        try:
            module = __import__(module_name)
            agent_class = getattr(module, class_name)
            agent = agent_class()
            print(f"\n▶️ Running {class_name}...")
            result = agent.run()
            results[class_name] = result
            print(f"   ✅ {class_name} completed.")
        except Exception as e:
            print(f"   ❌ {class_name} failed: {e}")
    print("\n📊 All agents executed. Reports saved to dist/intelligence_reports/")
    return results

if __name__ == "__main__":
    run_all_agents()
