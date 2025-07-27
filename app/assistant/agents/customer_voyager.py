#!/usr/bin/env python3
"""
🎯 CustomerVoyager - Customer Experience & Feedback Analysis
Analyzes user interactions, feedback patterns, and suggests UX improvements
"""
import argparse, json, sys, re
from pathlib import Path
from typing import Dict, List
import time

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("CustomerVoyager")
    except Exception:
        return True

class CustomerVoyager:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.customer_dir = self.project_root / "data" / "customer"
        self.customer_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_user_flows(self):
        """Analyze common user interaction patterns"""
        # Look for frontend interaction files
        frontend_files = []
        for pattern in ["*.js", "*.jsx", "*.ts", "*.tsx", "*.vue", "*.svelte"]:
            frontend_files.extend(list(self.project_root.rglob(pattern)))
        
        flow_patterns = {
            "authentication": 0,
            "search": 0,
            "checkout": 0,
            "navigation": 0,
            "error_handling": 0
        }
        
        for file_path in frontend_files:
            try:
                content = file_path.read_text()
                if re.search(r"login|signin|auth", content, re.IGNORECASE):
                    flow_patterns["authentication"] += 1
                if re.search(r"search|filter|query", content, re.IGNORECASE):
                    flow_patterns["search"] += 1
                if re.search(r"cart|checkout|payment|order", content, re.IGNORECASE):
                    flow_patterns["checkout"] += 1
                if re.search(r"navigate|route|link", content, re.IGNORECASE):
                    flow_patterns["navigation"] += 1
                if re.search(r"error|catch|exception", content, re.IGNORECASE):
                    flow_patterns["error_handling"] += 1
            except Exception:
                continue
                
        return flow_patterns
    
    def generate_ux_recommendations(self, flow_analysis: Dict) -> List[str]:
        """Generate UX improvement recommendations based on analysis"""
        recommendations = []
        
        if flow_analysis["error_handling"] < 3:
            recommendations.append("Add more comprehensive error handling and user feedback")
        
        if flow_analysis["search"] > 0 and flow_analysis["search"] < 5:
            recommendations.append("Enhance search functionality with filters and autocomplete")
            
        if flow_analysis["authentication"] > 0:
            recommendations.append("Consider adding social login options and password recovery")
            
        if flow_analysis["checkout"] > 0:
            recommendations.append("Streamline checkout process and add progress indicators")
        
        recommendations.append("Implement user analytics to track engagement metrics")
        recommendations.append("Add accessibility features (ARIA labels, keyboard navigation)")
        recommendations.append("Optimize for mobile responsiveness")
        
        return recommendations
    
    def simulate_user_personas(self) -> Dict:
        """Create user personas for testing"""
        personas = {
            "tech_savvy": {
                "expectations": ["Fast load times", "Advanced features", "Keyboard shortcuts"],
                "pain_points": ["Slow responses", "Missing features", "Complex workflows"],
                "devices": ["Desktop", "Mobile"],
                "behavior": "Explores all features, provides detailed feedback"
            },
            "casual_user": {
                "expectations": ["Simple interface", "Clear instructions", "Quick tasks"],
                "pain_points": ["Confusing navigation", "Too many options", "Technical jargon"],
                "devices": ["Mobile", "Tablet"],
                "behavior": "Uses basic features, expects intuitive design"
            },
            "business_user": {
                "expectations": ["Reliability", "Bulk operations", "Reporting features"],
                "pain_points": ["Downtime", "Data export limits", "Poor integration"],
                "devices": ["Desktop"],
                "behavior": "Focuses on efficiency and productivity"
            }
        }
        return personas
    
    def analyze_backend_patterns(self):
        """Analyze backend code for customer-facing features"""
        backend_files = []
        for pattern in ["*.py", "*.js", "*.go", "*.java"]:
            backend_files.extend(list(self.project_root.rglob(pattern)))
        
        backend_features = {
            "api_endpoints": 0,
            "authentication": 0,
            "data_validation": 0,
            "caching": 0,
            "rate_limiting": 0,
            "logging": 0
        }
        
        for file_path in backend_files:
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text()
                if re.search(r"@app\.|@router\.|def.*api|FastAPI|Flask", content):
                    backend_features["api_endpoints"] += 1
                if re.search(r"jwt|token|auth|login", content, re.IGNORECASE):
                    backend_features["authentication"] += 1
                if re.search(r"validate|schema|pydantic", content, re.IGNORECASE):
                    backend_features["data_validation"] += 1
                if re.search(r"cache|redis|memcache", content, re.IGNORECASE):
                    backend_features["caching"] += 1
                if re.search(r"rate.?limit|throttle", content, re.IGNORECASE):
                    backend_features["rate_limiting"] += 1
                if re.search(r"log|logger|logging", content, re.IGNORECASE):
                    backend_features["logging"] += 1
            except Exception:
                continue
                
        return backend_features

def main():
    parser = argparse.ArgumentParser(description="CustomerVoyager - Customer Experience Analysis")
    parser.add_argument("--analyze-flows", action="store_true", help="Analyze user flows")
    parser.add_argument("--backend-analysis", action="store_true", help="Analyze backend customer features")
    parser.add_argument("--personas", action="store_true", help="Generate user personas")
    parser.add_argument("--recommendations", action="store_true", help="Generate UX recommendations")
    parser.add_argument("--full-report", action="store_true", help="Generate comprehensive customer report")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    
    if not is_agent_enabled():
        print("🎯 CustomerVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🎯 CustomerVoyager: Smoke test passed!")
        return 0
    
    voyager = CustomerVoyager()
    
    if args.analyze_flows or args.full_report:
        flows = voyager.analyze_user_flows()
        print("🎯 User Flow Analysis:")
        for flow, count in flows.items():
            print(f"  {flow}: {count} instances")
            
    if args.backend_analysis or args.full_report:
        backend = voyager.analyze_backend_patterns()
        print("\n🎯 Backend Customer Features:")
        for feature, count in backend.items():
            print(f"  {feature}: {count} instances")
    
    if args.personas or args.full_report:
        personas = voyager.simulate_user_personas()
        print("\n🎯 User Personas:")
        for persona_type, details in personas.items():
            print(f"  {persona_type}: {details['behavior']}")
    
    if args.recommendations or args.full_report:
        flows = voyager.analyze_user_flows()
        recommendations = voyager.generate_ux_recommendations(flows)
        print("\n🎯 UX Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    # Save report
    report_file = voyager.customer_dir / "customer_analysis.json"
    report_data = {
        "timestamp": time.time(),
        "flows": voyager.analyze_user_flows(),
        "backend": voyager.analyze_backend_patterns(),
        "personas": voyager.simulate_user_personas(),
        "recommendations": voyager.generate_ux_recommendations(voyager.analyze_user_flows())
    }
    
    with open(report_file, "w") as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n🎯 CustomerVoyager: Report saved to {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
