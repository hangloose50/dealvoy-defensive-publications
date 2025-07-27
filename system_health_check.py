#!/usr/bin/env python3
"""
🔍 Dealvoy System Health Checker
Comprehensive audit of all 31+ Voyager agents and AI systems
"""

import sys
import json
import yaml
import time
from datetime import datetime
from pathlib import Path

def check_system_health():
    """Comprehensive system health check"""
    print("🔍 DEALVOY SYSTEM HEALTH AUDIT")
    print("=" * 60)
    
    health_report = {
        "audit_timestamp": datetime.now().isoformat(),
        "system_status": "checking",
        "agents": {},
        "ai_systems": {},
        "infrastructure": {},
        "security": {},
        "web_interfaces": {},
        "summary": {}
    }
    
    # Check Voyager Agents
    print("\n🤖 VOYAGER AGENTS STATUS:")
    agents_status = check_voyager_agents()
    health_report["agents"] = agents_status
    
    # Check AI Intelligence Layer
    print("\n🧠 AI INTELLIGENCE LAYER:")
    ai_status = check_ai_systems()
    health_report["ai_systems"] = ai_status
    
    # Check Infrastructure
    print("\n🏗️ INFRASTRUCTURE STATUS:")
    infra_status = check_infrastructure()
    health_report["infrastructure"] = infra_status
    
    # Check Security
    print("\n🔐 SECURITY STATUS:")
    security_status = check_security()
    health_report["security"] = security_status
    
    # Check Web Interfaces
    print("\n🌐 WEB INTERFACES:")
    web_status = check_web_interfaces()
    health_report["web_interfaces"] = web_status
    
    # Generate Summary
    summary = generate_summary(health_report)
    health_report["summary"] = summary
    health_report["system_status"] = "completed"
    
    # Save Health Report
    report_file = Path("dist/health_audit_report.json")
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(health_report, f, indent=2)
    
    print(f"\n📄 Health report saved: {report_file}")
    return health_report

def check_voyager_agents():
    """Check all Voyager agents from agents.yml"""
    agents_file = Path("app/assistant/agents/agents.yml")
    
    if not agents_file.exists():
        return {"status": "ERROR", "message": "agents.yml not found"}
    
    try:
        with open(agents_file, 'r') as f:
            agents_config = yaml.safe_load(f)
        
        total_agents = len(agents_config)
        enabled_agents = len([a for a in agents_config.values() if a.get('enabled', False)])
        disabled_agents = total_agents - enabled_agents
        
        # Categorize agents
        categories = {
            "core_business": ["DealScorerVoyager", "UngatingVoyager", "ScraperInfrastructureVoyager"],
            "web_ui": ["WebVoyager", "BrandVoyager", "AdminVoyager"],
            "ai_intelligence": ["TrendAIVoyager", "SupplierMatchAIVoyager", "CategoryRecommenderAIVoyager", 
                              "DealExplainerAIVoyager", "ProductClusterAIVoyager", "RiskForecasterAIVoyager",
                              "BrandRelationshipAIVoyager", "CashflowPredictorAIVoyager", "AutoOptimizerAIVoyager"],
            "security_toggles": ["PatentVoyager", "PatentResearchVoyager", "StripeVoyager"],
            "development": ["CodeVoyager", "SecurityVoyager", "PerformanceVoyager"]
        }
        
        category_status = {}
        for category, agent_names in categories.items():
            enabled_in_category = 0
            total_in_category = len(agent_names)
            for agent_name in agent_names:
                if agent_name in agents_config and agents_config[agent_name].get('enabled', False):
                    enabled_in_category += 1
            
            category_status[category] = {
                "enabled": enabled_in_category,
                "total": total_in_category,
                "percentage": round((enabled_in_category / total_in_category) * 100, 1) if total_in_category > 0 else 0
            }
        
        print(f"   Total Agents: {total_agents}")
        print(f"   Enabled: {enabled_agents}")
        print(f"   Disabled: {disabled_agents}")
        
        for category, status in category_status.items():
            status_icon = "✅" if status["percentage"] > 80 else "⚠️" if status["percentage"] > 50 else "❌"
            print(f"   {status_icon} {category.replace('_', ' ').title()}: {status['enabled']}/{status['total']} ({status['percentage']}%)")
        
        return {
            "status": "SUCCESS",
            "total_agents": total_agents,
            "enabled_agents": enabled_agents,
            "disabled_agents": disabled_agents,
            "categories": category_status,
            "health_score": round((enabled_agents / total_agents) * 100, 1)
        }
        
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def check_ai_systems():
    """Check AI intelligence layer systems"""
    ai_systems_dir = Path("app/ai_systems")
    
    if not ai_systems_dir.exists():
        return {"status": "ERROR", "message": "AI systems directory not found"}
    
    expected_systems = [
        "trend_ai.py", "supplier_match_ai.py", "category_recommender_ai.py",
        "deal_explainer_ai.py", "product_cluster_ai.py", "risk_forecaster_ai.py", 
        "brand_relationship_ai.py", "cashflow_predictor_ai.py", "auto_optimizer_ai.py"
    ]
    
    found_systems = []
    missing_systems = []
    
    for system in expected_systems:
        system_file = ai_systems_dir / system
        if system_file.exists():
            found_systems.append(system)
            print(f"   ✅ {system}")
        else:
            missing_systems.append(system)
            print(f"   ❌ {system} - MISSING")
    
    # Check orchestrator
    orchestrator_file = ai_systems_dir / "orchestrator.py"
    orchestrator_status = "✅" if orchestrator_file.exists() else "❌"
    print(f"   {orchestrator_status} orchestrator.py")
    
    return {
        "status": "SUCCESS" if len(missing_systems) == 0 else "WARNING",
        "total_expected": len(expected_systems),
        "found_systems": len(found_systems),
        "missing_systems": missing_systems,
        "orchestrator_available": orchestrator_file.exists(),
        "health_score": round((len(found_systems) / len(expected_systems)) * 100, 1)
    }

def check_infrastructure():
    """Check infrastructure components"""
    components = {
        "dealvoy_frontend": Path("dealvoy_frontend"),
        "web_landing": Path("dealvoy_frontend/web/index.html"),
        "customer_dashboard": Path("dealvoy_frontend/dashboard/index.html"),
        "admin_panel": Path("dealvoy_frontend/admin/index.html"),
        "real_pipeline_test": Path("test_real_pipeline.py"),
        "desktop_shortcuts": Path("create_ai_shortcuts.sh"),
        "web_shortcuts": Path("create_web_shortcuts.sh")
    }
    
    status = {}
    for component, path in components.items():
        exists = path.exists()
        status[component] = exists
        icon = "✅" if exists else "❌"
        print(f"   {icon} {component}: {path}")
    
    working_components = len([s for s in status.values() if s])
    total_components = len(status)
    
    return {
        "status": "SUCCESS" if working_components == total_components else "WARNING",
        "components": status,
        "working_components": working_components,
        "total_components": total_components,
        "health_score": round((working_components / total_components) * 100, 1)
    }

def check_security():
    """Check security configurations"""
    security_checks = {}
    
    # Check agents.yml for proper toggle configuration
    agents_file = Path("app/assistant/agents/agents.yml")
    if agents_file.exists():
        with open(agents_file, 'r') as f:
            agents_config = yaml.safe_load(f)
        
        # Security-sensitive agents should be disabled by default
        security_agents = ["PatentVoyager", "PatentResearchVoyager", "StripeVoyager"]
        secure_config = True
        
        for agent in security_agents:
            if agent in agents_config:
                enabled = agents_config[agent].get('enabled', False)
                if enabled:
                    secure_config = False
                    print(f"   ⚠️ {agent} is enabled (should be disabled for security)")
                else:
                    print(f"   ✅ {agent} properly disabled")
        
        security_checks["toggle_security"] = secure_config
    
    # Check for sensitive files
    sensitive_files = [
        "credentials.json",
        "google-credentials.json",
        ".env"
    ]
    
    for file in sensitive_files:
        if Path(file).exists():
            print(f"   ⚠️ Sensitive file detected: {file}")
            security_checks[f"sensitive_{file}"] = True
        else:
            print(f"   ✅ No sensitive file: {file}")
            security_checks[f"sensitive_{file}"] = False
    
    return {
        "status": "SUCCESS" if security_checks.get("toggle_security", True) else "WARNING",
        "checks": security_checks,
        "security_score": 85 if security_checks.get("toggle_security", True) else 60
    }

def check_web_interfaces():
    """Check web interface accessibility"""
    interfaces = {
        "landing_page": "dealvoy_frontend/web/index.html",
        "customer_dashboard": "dealvoy_frontend/dashboard/index.html", 
        "admin_panel": "dealvoy_frontend/admin/index.html"
    }
    
    status = {}
    for interface, path in interfaces.items():
        file_path = Path(path)
        exists = file_path.exists()
        
        if exists:
            # Check file size as basic validation
            file_size = file_path.stat().st_size
            valid_size = file_size > 1000  # At least 1KB
            status[interface] = {"exists": True, "valid_size": valid_size, "size_kb": round(file_size/1024, 1)}
            icon = "✅" if valid_size else "⚠️"
        else:
            status[interface] = {"exists": False, "valid_size": False, "size_kb": 0}
            icon = "❌"
        
        print(f"   {icon} {interface}: {status[interface]}")
    
    working_interfaces = len([s for s in status.values() if s["exists"] and s["valid_size"]])
    total_interfaces = len(status)
    
    return {
        "status": "SUCCESS" if working_interfaces == total_interfaces else "WARNING",
        "interfaces": status,
        "working_interfaces": working_interfaces,
        "total_interfaces": total_interfaces,
        "health_score": round((working_interfaces / total_interfaces) * 100, 1)
    }

def generate_summary(health_report):
    """Generate overall system summary"""
    components = ["agents", "ai_systems", "infrastructure", "security", "web_interfaces"]
    
    total_score = 0
    component_count = 0
    
    for component in components:
        if component in health_report and "health_score" in health_report[component]:
            total_score += health_report[component]["health_score"]
            component_count += 1
    
    overall_score = round(total_score / component_count, 1) if component_count > 0 else 0
    
    if overall_score >= 90:
        status = "EXCELLENT"
        status_icon = "🟢"
    elif overall_score >= 75:
        status = "GOOD"
        status_icon = "🟡"
    elif overall_score >= 60:
        status = "WARNING"
        status_icon = "🟠"
    else:
        status = "CRITICAL"
        status_icon = "🔴"
    
    print(f"\n{status_icon} OVERALL SYSTEM STATUS: {status}")
    print(f"📊 Health Score: {overall_score}%")
    
    # Recommendations
    recommendations = []
    
    if health_report.get("agents", {}).get("health_score", 0) < 90:
        recommendations.append("Enable additional Voyager agents for full functionality")
    
    if health_report.get("ai_systems", {}).get("health_score", 0) < 100:
        recommendations.append("Complete AI systems implementation")
    
    if health_report.get("security", {}).get("security_score", 0) < 80:
        recommendations.append("Review and secure sensitive agent configurations")
    
    if recommendations:
        print("\n🎯 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    return {
        "overall_score": overall_score,
        "status": status,
        "status_icon": status_icon,
        "recommendations": recommendations,
        "launch_ready": overall_score >= 85
    }

if __name__ == "__main__":
    health_report = check_system_health()
    
    if health_report["summary"]["launch_ready"]:
        print("\n🚀 SYSTEM IS LAUNCH READY!")
    else:
        print("\n⚠️ SYSTEM NEEDS ATTENTION BEFORE LAUNCH")
    
    print(f"\nFor detailed report, see: dist/health_audit_report.json")
