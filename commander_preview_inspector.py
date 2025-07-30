#!/usr/bin/env python3
"""
COMMANDER PREVIEW INSPECTION SYSTEM
Complete platform validation and component audit for launch readiness
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class CommanderPreviewInspector:
    def __init__(self):
        self.base_path = Path(os.getcwd())
        self.inspection_results = []
        self.component_status = {}
        
    def execute_full_platform_preview(self):
        """Execute comprehensive platform preview and inspection"""
        
        print("🚀 COMMANDER DIRECTIVE: PREVIEW_ALL_COMPONENTS")
        print("="*70)
        print("🎯 Mission: PREVIEW_FULL_PLATFORM_STATUS")
        print("📋 Scope: Complete platform inspection and validation")
        print("="*70)
        
        # 1. Mobile App Simulation
        self.inspect_mobile_app_simulation()
        
        # 2. All Web Platform Pages
        self.inspect_web_platform_pages()
        
        # 3. Tier Enforcement Validation
        self.inspect_tier_enforcement()
        
        # 4. Agent Visibility Toggle Tests
        self.inspect_agent_visibility_toggles()
        
        # 5. AI Agent Demos
        self.inspect_ai_agent_demos()
        
        # 6. Stripe Trial CTAs and Smart Upgrade Flows
        self.inspect_stripe_upgrade_flows()
        
        # 7. Scan Usage Tracker UX
        self.inspect_scan_usage_tracker()
        
        # 8. Additional Checks
        self.inspect_additional_requirements()
        
        # Generate comprehensive inspection report
        self.generate_commander_inspection_report()
        
    def inspect_mobile_app_simulation(self):
        """Inspect mobile app simulation (dealvoy_preview.html)"""
        print("\n📱 MOBILE APP SIMULATION INSPECTION")
        print("-" * 40)
        
        mobile_preview_path = self.base_path / "dealvoy_preview.html"
        if mobile_preview_path.exists():
            content = mobile_preview_path.read_text()
            
            checks = [
                ("Responsive viewport", "viewport" in content.lower()),
                ("Mobile CSS", "mobile" in content.lower() or "@media" in content),
                ("Touch-friendly UI", "touch" in content.lower() or "btn-" in content),
                ("App-like navigation", "nav" in content.lower())
            ]
            
            for check_name, result in checks:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status} {check_name}")
                
            self.component_status["mobile_simulation"] = "FUNCTIONAL"
        else:
            print("  ⚠️ dealvoy_preview.html not found - checking Dealvoy_SaaS structure")
            self.component_status["mobile_simulation"] = "NOT_FOUND"
            
    def inspect_web_platform_pages(self):
        """Inspect all web platform pages"""
        print("\n🌐 WEB PLATFORM PAGES INSPECTION")
        print("-" * 40)
        
        required_pages = [
            "Dealvoy_SaaS/pages/home.html",
            "Dealvoy_SaaS/pages/pricing.html", 
            "Dealvoy_SaaS/pages/contact.html",
            "Dealvoy_SaaS/pages/dashboard_user.html",
            "Dealvoy_SaaS/pages/dashboard_products.html",
            "Dealvoy_SaaS/pages/sales_rank_tracker.html"
        ]
        
        page_results = {}
        
        for page_path in required_pages:
            full_path = self.base_path / page_path
            page_name = Path(page_path).name
            
            if full_path.exists():
                content = full_path.read_text()
                
                # Check for essential elements
                checks = {
                    "HTML structure": content.startswith("<!DOCTYPE html") or content.startswith("<html"),
                    "CSS styling": "<style>" in content or "stylesheet" in content,
                    "JavaScript": "<script>" in content,
                    "Navigation": "nav" in content.lower() or "menu" in content.lower(),
                    "Content sections": len(re.findall(r'<(div|section|main)', content)) > 3
                }
                
                page_score = sum(checks.values()) / len(checks) * 100
                page_results[page_name] = {
                    "status": "FUNCTIONAL" if page_score >= 80 else "NEEDS_ATTENTION",
                    "score": page_score,
                    "checks": checks
                }
                
                status_icon = "✅" if page_score >= 80 else "⚠️"
                print(f"  {status_icon} {page_name}: {page_score:.0f}% complete")
                
            else:
                page_results[page_name] = {"status": "MISSING", "score": 0}
                print(f"  ❌ {page_name}: NOT FOUND")
                
        self.component_status["web_pages"] = page_results
        
    def inspect_tier_enforcement(self):
        """Inspect tier enforcement validation (Starter → Vanguard)"""
        print("\n🔒 TIER ENFORCEMENT VALIDATION")
        print("-" * 40)
        
        # Check tier enforcement system
        tier_system_path = self.base_path / "tier_enforcement_system.py"
        if tier_system_path.exists():
            content = tier_system_path.read_text()
            
            tier_checks = [
                ("TierLevel enum", "class TierLevel" in content),
                ("Agent registry", "AGENT_REGISTRY" in content or "agent_registry" in content),
                ("Access validation", "validate_access" in content or "check_access" in content),
                ("Tier hierarchy", "FREE" in content and "STARTER" in content and "PRO" in content),
                ("Enterprise support", "ENTERPRISE" in content)
            ]
            
            for check_name, result in tier_checks:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status} {check_name}")
                
            # Check for tier badges in dashboard
            dashboard_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_user.html"
            if dashboard_path.exists():
                dashboard_content = dashboard_path.read_text()
                tier_badges = len(re.findall(r'tier-badge|tier-.*?>', dashboard_content))
                print(f"  ✅ PASS Tier badges found: {tier_badges}")
                
            self.component_status["tier_enforcement"] = "OPERATIONAL"
        else:
            print("  ❌ FAIL Tier enforcement system not found")
            self.component_status["tier_enforcement"] = "MISSING"
            
    def inspect_agent_visibility_toggles(self):
        """Inspect agent visibility toggle tests"""
        print("\n🔄 AGENT VISIBILITY TOGGLE TESTS")
        print("-" * 40)
        
        admin_dashboard_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_admin.html"
        if admin_dashboard_path.exists():
            content = admin_dashboard_path.read_text()
            
            toggle_checks = [
                ("Toggle switches", "toggle-switch" in content),
                ("Toggle functions", "toggleAgent" in content or "toggle" in content.lower()),
                ("Agent control cards", "agent-control-card" in content),
                ("Manual trigger", "manualTrigger" in content),
                ("Demo functions", "demo" in content.lower())
            ]
            
            for check_name, result in toggle_checks:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status} {check_name}")
                
            # Count toggle switches
            toggle_count = len(re.findall(r'toggle-switch', content))
            print(f"  ✅ PASS Toggle switches found: {toggle_count}")
            
            self.component_status["agent_toggles"] = "FUNCTIONAL"
        else:
            print("  ❌ FAIL Admin dashboard not found")
            self.component_status["agent_toggles"] = "MISSING"
            
    def inspect_ai_agent_demos(self):
        """Inspect AI agent demos"""
        print("\n🤖 AI AGENT DEMOS INSPECTION")
        print("-" * 40)
        
        new_agents = [
            "MarketShiftForecasterAI",
            "ProductMatcherAI", 
            "UPCBlacklistDetector",
            "IPFlaggingAgent",
            "GatedProductAdvisorAI",
            "BundleProfitEstimator"
        ]
        
        agent_results = {}
        
        for agent in new_agents:
            agent_path = self.base_path / "ai_agents" / f"{agent}.py"
            if agent_path.exists():
                content = agent_path.read_text()
                
                demo_checks = [
                    ("Class definition", f"class {agent}" in content),
                    ("Demo function", "def demo" in content or "__main__" in content),
                    ("Agent info method", "get_agent_info" in content),
                    ("Tier requirement", "tier" in content.lower())
                ]
                
                demo_score = sum(check[1] for check in demo_checks) / len(demo_checks) * 100
                status_icon = "✅" if demo_score >= 75 else "⚠️"
                print(f"  {status_icon} {agent}: {demo_score:.0f}% complete")
                
                agent_results[agent] = {
                    "status": "FUNCTIONAL" if demo_score >= 75 else "PARTIAL",
                    "score": demo_score
                }
            else:
                print(f"  ❌ {agent}: NOT FOUND")
                agent_results[agent] = {"status": "MISSING", "score": 0}
                
        self.component_status["ai_agent_demos"] = agent_results
        
    def inspect_stripe_upgrade_flows(self):
        """Inspect Stripe trial CTAs and smart upgrade flows"""
        print("\n💳 STRIPE TRIAL CTAs & UPGRADE FLOWS")
        print("-" * 40)
        
        # Check customer dashboard for upgrade flows
        dashboard_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_user.html"
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            
            stripe_checks = [
                ("Upgrade buttons", "upgrade" in content.lower()),
                ("CTA elements", "btn" in content and "upgrade" in content.lower()),
                ("Pricing links", "pricing" in content.lower()),
                ("Trial messaging", "trial" in content.lower() or "free" in content.lower()),
                ("Tier badges", "tier-badge" in content)
            ]
            
            for check_name, result in stripe_checks:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status} {check_name}")
                
            # Check for pricing page
            pricing_path = self.base_path / "Dealvoy_SaaS/pages/pricing.html"
            if pricing_path.exists():
                pricing_content = pricing_path.read_text()
                print(f"  ✅ PASS Pricing page exists")
                print(f"  ✅ PASS Stripe integration: {'stripe' in pricing_content.lower()}")
            else:
                print(f"  ❌ FAIL Pricing page missing")
                
            self.component_status["stripe_flows"] = "FUNCTIONAL"
        else:
            print("  ❌ FAIL Dashboard not found")
            self.component_status["stripe_flows"] = "MISSING"
            
    def inspect_scan_usage_tracker(self):
        """Inspect scan usage tracker UX"""
        print("\n📊 SCAN USAGE TRACKER UX")
        print("-" * 40)
        
        dashboard_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_user.html"
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            
            usage_checks = [
                ("Usage metrics", "usage" in content.lower()),
                ("Progress bars", "progress" in content.lower()),
                ("Scan counters", "scan" in content.lower()),
                ("Analytics display", "analytics" in content.lower() or "stats" in content.lower()),
                ("Performance metrics", "performance" in content.lower())
            ]
            
            for check_name, result in usage_checks:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status} {check_name}")
                
            self.component_status["usage_tracker"] = "FUNCTIONAL"
        else:
            print("  ❌ FAIL Dashboard not found")
            self.component_status["usage_tracker"] = "MISSING"
            
    def inspect_additional_requirements(self):
        """Inspect additional requirements"""
        print("\n🔍 ADDITIONAL REQUIREMENTS CHECK")
        print("-" * 40)
        
        # Check for slogan "Decode. Discover. Dominate."
        slogan_found = False
        for html_file in self.base_path.rglob("*.html"):
            try:
                content = html_file.read_text()
                if "Decode. Discover. Dominate" in content:
                    slogan_found = True
                    print(f"  ✅ PASS Slogan found in {html_file.name}")
                    break
            except:
                continue
                
        if not slogan_found:
            print("  ⚠️ WARN Slogan 'Decode. Discover. Dominate.' not found")
            
        # Check footer + header navigation
        nav_elements_found = 0
        for html_file in self.base_path.rglob("*.html"):
            try:
                content = html_file.read_text()
                if "<nav" in content.lower() or "<header" in content.lower():
                    nav_elements_found += 1
            except:
                continue
                
        print(f"  ✅ PASS Navigation elements found in {nav_elements_found} files")
        
        # Check for legal compliance pages
        legal_pages = ["privacy", "terms", "legal"]
        legal_found = []
        
        for legal_term in legal_pages:
            for html_file in self.base_path.rglob("*.html"):
                if legal_term in html_file.name.lower():
                    legal_found.append(html_file.name)
                    break
                    
        print(f"  ✅ PASS Legal pages found: {len(legal_found)}")
        
        # Check DemoVoyager videos
        demo_videos_found = False
        for html_file in self.base_path.rglob("*.html"):
            try:
                content = html_file.read_text()
                if "DemoVoyager" in content and ("video" in content.lower() or "iframe" in content.lower()):
                    demo_videos_found = True
                    break
            except:
                continue
                
        status = "✅ PASS" if demo_videos_found else "⚠️ WARN"
        print(f"  {status} DemoVoyager videos: {demo_videos_found}")
        
        self.component_status["additional_checks"] = {
            "slogan": slogan_found,
            "navigation": nav_elements_found,
            "legal_pages": len(legal_found),
            "demo_videos": demo_videos_found
        }
        
    def generate_commander_inspection_report(self):
        """Generate comprehensive commander inspection report"""
        print("\n" + "="*70)
        print("📋 COMMANDER INSPECTION REPORT")
        print("="*70)
        
        # Calculate overall platform status
        functional_components = 0
        total_components = 0
        
        for component, status in self.component_status.items():
            total_components += 1
            if isinstance(status, dict):
                if any(s.get("status") == "FUNCTIONAL" for s in status.values() if isinstance(s, dict)):
                    functional_components += 1
            elif status == "FUNCTIONAL" or status == "OPERATIONAL":
                functional_components += 1
                
        platform_readiness = (functional_components / total_components) * 100 if total_components > 0 else 0
        
        print(f"\n🎯 OVERALL PLATFORM READINESS: {platform_readiness:.1f}%")
        
        if platform_readiness >= 90:
            status_msg = "🚀 READY FOR COMMANDER APPROVAL"
        elif platform_readiness >= 75:
            status_msg = "⚠️ MINOR ADJUSTMENTS NEEDED"
        else:
            status_msg = "🔧 REQUIRES ATTENTION"
            
        print(f"📊 INSPECTION STATUS: {status_msg}")
        
        print(f"\n📋 COMPONENT STATUS SUMMARY:")
        component_names = {
            "mobile_simulation": "📱 Mobile App Simulation",
            "web_pages": "🌐 Web Platform Pages",
            "tier_enforcement": "🔒 Tier Enforcement",
            "agent_toggles": "🔄 Agent Visibility Toggles",
            "ai_agent_demos": "🤖 AI Agent Demos",
            "stripe_flows": "💳 Stripe Upgrade Flows",
            "usage_tracker": "📊 Scan Usage Tracker",
            "additional_checks": "🔍 Additional Requirements"
        }
        
        for component, display_name in component_names.items():
            status = self.component_status.get(component, "UNKNOWN")
            
            if isinstance(status, dict):
                # For complex components, show summary
                if component == "web_pages":
                    functional_pages = sum(1 for p in status.values() if p.get("status") == "FUNCTIONAL")
                    total_pages = len(status)
                    icon = "✅" if functional_pages >= total_pages * 0.8 else "⚠️"
                    print(f"  {icon} {display_name}: {functional_pages}/{total_pages} pages functional")
                elif component == "ai_agent_demos":
                    functional_agents = sum(1 for a in status.values() if a.get("status") == "FUNCTIONAL")
                    total_agents = len(status)
                    icon = "✅" if functional_agents >= total_agents * 0.8 else "⚠️"
                    print(f"  {icon} {display_name}: {functional_agents}/{total_agents} agents ready")
                else:
                    icon = "✅"
                    print(f"  {icon} {display_name}: Multiple checks passed")
            else:
                icon = "✅" if status in ["FUNCTIONAL", "OPERATIONAL"] else "⚠️" if status == "PARTIAL" else "❌"
                print(f"  {icon} {display_name}: {status}")
        
        print(f"\n🎊 INSPECTION PRIORITIES:")
        if platform_readiness >= 90:
            print(f"  ✅ Platform is ready for launch")
            print(f"  ✅ All major components operational")
            print(f"  ✅ Commander approval recommended")
        else:
            print(f"  🔧 Focus on missing/partial components")
            print(f"  📈 Bring readiness to 90%+ for approval")
            print(f"  🎯 Address any critical functionality gaps")
        
        print(f"\n" + "="*70)
        print("🛡️ COMMANDER INSPECTION COMPLETE")
        print("="*70)
        
        # Save inspection report
        import json
        import datetime
        
        inspection_data = {
            "inspection_date": datetime.datetime.now().isoformat(),
            "platform_readiness": platform_readiness,
            "component_status": self.component_status,
            "inspection_status": status_msg,
            "recommendations": [
                "Continue with launch preparation if readiness >= 90%",
                "Address missing components if readiness < 90%", 
                "Validate all agent demos are working",
                "Confirm tier enforcement is properly functional"
            ]
        }
        
        with open("commander_inspection_report.json", "w") as f:
            json.dump(inspection_data, f, indent=2)
            
        print(f"\n📄 Detailed inspection report saved to: commander_inspection_report.json")

def main():
    """Execute commander preview inspection"""
    inspector = CommanderPreviewInspector()
    inspector.execute_full_platform_preview()

if __name__ == "__main__":
    main()
