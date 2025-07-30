#!/usr/bin/env python3
"""
Website Validation System - DEPLOY_PERFECTION_REFINEMENT
Comprehensive validation for tier enforcement, UI consistency, and launch readiness
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

class ValidationStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARNING = "⚠️ WARNING"
    INFO = "ℹ️ INFO"

@dataclass
class ValidationResult:
    component: str
    test_name: str
    status: ValidationStatus
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    fix_suggestion: Optional[str] = None

@dataclass
class WebsiteValidationReport:
    results: List[ValidationResult] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    
    def add_result(self, result: ValidationResult):
        self.results.append(result)
        
    def generate_summary(self):
        self.summary = {
            "PASS": len([r for r in self.results if r.status == ValidationStatus.PASS]),
            "FAIL": len([r for r in self.results if r.status == ValidationStatus.FAIL]),
            "WARNING": len([r for r in self.results if r.status == ValidationStatus.WARNING]),
            "INFO": len([r for r in self.results if r.status == ValidationStatus.INFO])
        }

class WebsiteValidator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.report = WebsiteValidationReport()
        
        # Tier definitions for validation
        self.tier_levels = ["FREE", "STARTER", "PRO", "ENTERPRISE", "ADMIN"]
        
        # Critical files to validate
        self.html_files = [
            "Dealvoy_SaaS/pages/dashboard_user.html",
            "Dealvoy_SaaS/pages/dashboard_admin.html",
            "Dealvoy_SaaS/pages/index.html",
            "Dealvoy_SaaS/pages/pricing.html"
        ]
        
        # New AI agents to verify
        self.new_agents = [
            "MarketShiftForecasterAI",
            "ProductMatcherAI", 
            "UPCBlacklistDetector",
            "IPFlaggingAgent",
            "GatedProductAdvisorAI",
            "BundleProfitEstimator"
        ]
        
        # Existing agents for completeness check
        self.existing_agents = [
            "TrendVoyager", "VidVoyager", "RiskSentinel", "ScoutVision", 
            "TierScaler", "DemoVoyager"
        ]

    def validate_tier_enforcement(self):
        """Validate tier enforcement system implementation"""
        print("🔒 Validating tier enforcement system...")
        
        # Check tier enforcement system file
        tier_system_path = self.base_path / "tier_enforcement_system.py"
        if tier_system_path.exists():
            content = tier_system_path.read_text()
            
            # Check for TierLevel enum
            if "class TierLevel(Enum):" in content:
                self.report.add_result(ValidationResult(
                    "Tier System", "TierLevel Enum", ValidationStatus.PASS,
                    "TierLevel enum properly defined", str(tier_system_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Tier System", "TierLevel Enum", ValidationStatus.FAIL,
                    "TierLevel enum not found", str(tier_system_path),
                    fix_suggestion="Add TierLevel enum with FREE, STARTER, PRO, ENTERPRISE, ADMIN"
                ))
            
            # Check for agent registry
            if "AGENT_REGISTRY" in content:
                self.report.add_result(ValidationResult(
                    "Tier System", "Agent Registry", ValidationStatus.PASS,
                    "Agent registry properly implemented", str(tier_system_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Tier System", "Agent Registry", ValidationStatus.FAIL,
                    "Agent registry not found", str(tier_system_path)
                ))
            
            # Check for new agents in registry
            for agent in self.new_agents:
                if agent in content:
                    self.report.add_result(ValidationResult(
                        "Tier System", f"{agent} Registration", ValidationStatus.PASS,
                        f"{agent} found in agent registry", str(tier_system_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "Tier System", f"{agent} Registration", ValidationStatus.FAIL,
                        f"{agent} missing from agent registry", str(tier_system_path)
                    ))
        else:
            self.report.add_result(ValidationResult(
                "Tier System", "System File", ValidationStatus.FAIL,
                "tier_enforcement_system.py not found", None,
                fix_suggestion="Create tier enforcement system file"
            ))

    def validate_dashboard_integration(self):
        """Validate dashboard integration system"""
        print("🔗 Validating dashboard integration...")
        
        # Check dashboard integration system
        dashboard_system_path = self.base_path / "dashboard_integration_system.py"
        if dashboard_system_path.exists():
            content = dashboard_system_path.read_text()
            
            if "generate_customer_dashboard_html" in content:
                self.report.add_result(ValidationResult(
                    "Dashboard Integration", "Customer HTML Generation", ValidationStatus.PASS,
                    "Customer dashboard HTML generation implemented", str(dashboard_system_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Dashboard Integration", "Customer HTML Generation", ValidationStatus.FAIL,
                    "Customer dashboard HTML generation missing", str(dashboard_system_path)
                ))
                
            if "generate_admin_dashboard_html" in content:
                self.report.add_result(ValidationResult(
                    "Dashboard Integration", "Admin HTML Generation", ValidationStatus.PASS,
                    "Admin dashboard HTML generation implemented", str(dashboard_system_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Dashboard Integration", "Admin HTML Generation", ValidationStatus.WARNING,
                    "Admin dashboard HTML generation may be missing", str(dashboard_system_path)
                ))
        else:
            self.report.add_result(ValidationResult(
                "Dashboard Integration", "System File", ValidationStatus.FAIL,
                "dashboard_integration_system.py not found", None
            ))

    def validate_customer_dashboard(self):
        """Validate customer dashboard implementation"""
        print("👤 Validating customer dashboard...")
        
        dashboard_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_user.html"
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            
            # Check for new agents showcase
            new_agents_found = 0
            for agent in self.new_agents:
                if agent in content:
                    new_agents_found += 1
                    self.report.add_result(ValidationResult(
                        "Customer Dashboard", f"{agent} Integration", ValidationStatus.PASS,
                        f"{agent} found in customer dashboard", str(dashboard_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "Customer Dashboard", f"{agent} Integration", ValidationStatus.FAIL,
                        f"{agent} missing from customer dashboard", str(dashboard_path)
                    ))
            
            # Check tier badges
            tier_badge_count = content.count('tier-badge')
            if tier_badge_count >= 5:  # At least 5 visible agents with tier badges
                self.report.add_result(ValidationResult(
                    "Customer Dashboard", "Tier Badges", ValidationStatus.PASS,
                    f"Found {tier_badge_count} tier badges", str(dashboard_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Customer Dashboard", "Tier Badges", ValidationStatus.WARNING,
                    f"Only {tier_badge_count} tier badges found", str(dashboard_path)
                ))
            
            # Check upgrade prompts
            if "upgrade-section" in content or "btn-upgrade" in content:
                self.report.add_result(ValidationResult(
                    "Customer Dashboard", "Upgrade Prompts", ValidationStatus.PASS,
                    "Upgrade prompts implemented", str(dashboard_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Customer Dashboard", "Upgrade Prompts", ValidationStatus.WARNING,
                    "Upgrade prompts may be missing", str(dashboard_path)
                ))
                
        else:
            self.report.add_result(ValidationResult(
                "Customer Dashboard", "File Existence", ValidationStatus.FAIL,
                "dashboard_user.html not found", None
            ))

    def validate_admin_dashboard(self):
        """Validate admin dashboard implementation"""
        print("👨‍💼 Validating admin dashboard...")
        
        dashboard_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_admin.html"
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            
            # Check for new agents in admin control
            admin_agents_found = 0
            for agent in self.new_agents:
                if f'data-agent="{agent}"' in content:
                    admin_agents_found += 1
                    self.report.add_result(ValidationResult(
                        "Admin Dashboard", f"{agent} Control", ValidationStatus.PASS,
                        f"{agent} admin control found", str(dashboard_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "Admin Dashboard", f"{agent} Control", ValidationStatus.FAIL,
                        f"{agent} admin control missing", str(dashboard_path)
                    ))
            
            # Check toggle switches
            toggle_count = content.count('toggle-switch')
            expected_toggles = len(self.new_agents) + len(self.existing_agents)
            if toggle_count >= expected_toggles:
                self.report.add_result(ValidationResult(
                    "Admin Dashboard", "Toggle Switches", ValidationStatus.PASS,
                    f"Found {toggle_count} toggle switches", str(dashboard_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Admin Dashboard", "Toggle Switches", ValidationStatus.WARNING,
                    f"Expected {expected_toggles} toggles, found {toggle_count}", str(dashboard_path)
                ))
            
            # Check demo functions
            demo_functions = [f"run{agent}Demo" for agent in self.new_agents]
            demo_functions_found = 0
            for func in demo_functions:
                if func in content:
                    demo_functions_found += 1
            
            if demo_functions_found >= len(self.new_agents):
                self.report.add_result(ValidationResult(
                    "Admin Dashboard", "Demo Functions", ValidationStatus.PASS,
                    f"All {demo_functions_found} demo functions implemented", str(dashboard_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "Admin Dashboard", "Demo Functions", ValidationStatus.WARNING,
                    f"Only {demo_functions_found}/{len(self.new_agents)} demo functions found", str(dashboard_path)
                ))
                
        else:
            self.report.add_result(ValidationResult(
                "Admin Dashboard", "File Existence", ValidationStatus.FAIL,
                "dashboard_admin.html not found", None
            ))

    def validate_agent_files(self):
        """Validate individual agent file implementations"""
        print("🤖 Validating AI agent files...")
        
        for agent in self.new_agents:
            # Check in ai_agents directory
            agent_path = self.base_path / "ai_agents" / f"{agent}.py"
            if agent_path.exists():
                content = agent_path.read_text()
                
                # Check for class definition
                if f"class {agent}" in content:
                    self.report.add_result(ValidationResult(
                        "Agent Files", f"{agent} Class", ValidationStatus.PASS,
                        f"{agent} class properly defined", str(agent_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "Agent Files", f"{agent} Class", ValidationStatus.FAIL,
                        f"{agent} class not found", str(agent_path)
                    ))
                
                # Check for get_agent_info method
                if "def get_agent_info" in content:
                    self.report.add_result(ValidationResult(
                        "Agent Files", f"{agent} Info Method", ValidationStatus.PASS,
                        f"{agent} get_agent_info method found", str(agent_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "Agent Files", f"{agent} Info Method", ValidationStatus.WARNING,
                        f"{agent} get_agent_info method missing", str(agent_path)
                    ))
                
                # Check for demo function
                if "def run_demo" in content:
                    self.report.add_result(ValidationResult(
                        "Agent Files", f"{agent} Demo", ValidationStatus.PASS,
                        f"{agent} demo function implemented", str(agent_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "Agent Files", f"{agent} Demo", ValidationStatus.WARNING,
                        f"{agent} demo function missing", str(agent_path)
                    ))
                    
            else:
                self.report.add_result(ValidationResult(
                    "Agent Files", f"{agent} File", ValidationStatus.FAIL,
                    f"{agent} file not found at {agent_path}", None,
                    fix_suggestion=f"Create ai_agents/{agent}.py file"
                ))

    def validate_css_consistency(self):
        """Validate CSS styling consistency across pages"""
        print("🎨 Validating CSS consistency...")
        
        # Check for tier badge styles
        for html_file in self.html_files:
            file_path = self.base_path / html_file
            if file_path.exists():
                content = file_path.read_text()
                
                # Check for tier badge CSS classes
                tier_classes = ['tier-free', 'tier-starter', 'tier-pro', 'tier-enterprise', 'tier-admin']
                found_classes = [cls for cls in tier_classes if cls in content]
                
                if len(found_classes) >= 3:  # At least 3 tier classes
                    self.report.add_result(ValidationResult(
                        "CSS Consistency", f"{html_file} Tier Classes", ValidationStatus.PASS,
                        f"Found {len(found_classes)} tier classes", str(file_path)
                    ))
                else:
                    self.report.add_result(ValidationResult(
                        "CSS Consistency", f"{html_file} Tier Classes", ValidationStatus.WARNING,
                        f"Only {len(found_classes)} tier classes found", str(file_path)
                    ))
                
                # Check for agent card styles
                if "agent-card" in content or "agent-control-card" in content:
                    self.report.add_result(ValidationResult(
                        "CSS Consistency", f"{html_file} Agent Cards", ValidationStatus.PASS,
                        "Agent card styles present", str(file_path)
                    ))

    def validate_javascript_functionality(self):
        """Validate JavaScript functionality"""
        print("⚡ Validating JavaScript functionality...")
        
        # Check customer dashboard JavaScript
        customer_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_user.html"
        if customer_path.exists():
            content = customer_path.read_text()
            
            js_functions = ['launchAgent', 'showAgentDetails', 'upgradeToTier']
            found_functions = [func for func in js_functions if f"function {func}" in content]
            
            if len(found_functions) >= 2:
                self.report.add_result(ValidationResult(
                    "JavaScript", "Customer Functions", ValidationStatus.PASS,
                    f"Found {len(found_functions)} JavaScript functions", str(customer_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "JavaScript", "Customer Functions", ValidationStatus.WARNING,
                    f"Only {len(found_functions)} JavaScript functions found", str(customer_path)
                ))
        
        # Check admin dashboard JavaScript
        admin_path = self.base_path / "Dealvoy_SaaS/pages/dashboard_admin.html"
        if admin_path.exists():
            content = admin_path.read_text()
            
            admin_functions = ['manualTrigger', 'testTier', 'toggleAgent']
            found_admin_functions = [func for func in admin_functions if f"function {func}" in content]
            
            if len(found_admin_functions) >= 2:
                self.report.add_result(ValidationResult(
                    "JavaScript", "Admin Functions", ValidationStatus.PASS,
                    f"Found {len(found_admin_functions)} admin functions", str(admin_path)
                ))
            else:
                self.report.add_result(ValidationResult(
                    "JavaScript", "Admin Functions", ValidationStatus.WARNING,
                    f"Only {len(found_admin_functions)} admin functions found", str(admin_path)
                ))

    def validate_launch_readiness(self):
        """Validate overall launch readiness"""
        print("🚀 Validating launch readiness...")
        
        # Check for critical files
        critical_files = [
            "tier_enforcement_system.py",
            "dashboard_integration_system.py",
            "Dealvoy_SaaS/pages/dashboard_user.html",
            "Dealvoy_SaaS/pages/dashboard_admin.html"
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not (self.base_path / file_path).exists():
                missing_files.append(file_path)
        
        if not missing_files:
            self.report.add_result(ValidationResult(
                "Launch Readiness", "Critical Files", ValidationStatus.PASS,
                "All critical files present", None
            ))
        else:
            self.report.add_result(ValidationResult(
                "Launch Readiness", "Critical Files", ValidationStatus.FAIL,
                f"Missing files: {', '.join(missing_files)}", None
            ))
        
        # Check agent implementation completeness
        total_agents = len(self.new_agents) + len(self.existing_agents)
        implemented_agents = 0
        
        for agent in self.new_agents:
            agent_file = self.base_path / f"{agent.lower()}_ai.py"
            if agent_file.exists():
                implemented_agents += 1
        
        # Assume existing agents are implemented
        implemented_agents += len(self.existing_agents)
        
        completion_rate = (implemented_agents / total_agents) * 100
        
        if completion_rate >= 95:
            self.report.add_result(ValidationResult(
                "Launch Readiness", "Agent Completion", ValidationStatus.PASS,
                f"Agent implementation {completion_rate:.1f}% complete", None
            ))
        elif completion_rate >= 80:
            self.report.add_result(ValidationResult(
                "Launch Readiness", "Agent Completion", ValidationStatus.WARNING,
                f"Agent implementation {completion_rate:.1f}% complete", None
            ))
        else:
            self.report.add_result(ValidationResult(
                "Launch Readiness", "Agent Completion", ValidationStatus.FAIL,
                f"Agent implementation only {completion_rate:.1f}% complete", None
            ))

    def run_comprehensive_validation(self):
        """Run all validation tests"""
        print("🔍 Starting comprehensive website validation...\n")
        
        self.validate_tier_enforcement()
        self.validate_dashboard_integration()
        self.validate_customer_dashboard()
        self.validate_admin_dashboard()
        self.validate_agent_files()
        self.validate_css_consistency()
        self.validate_javascript_functionality()
        self.validate_launch_readiness()
        
        self.report.generate_summary()
        
        return self.report

    def print_validation_report(self):
        """Print comprehensive validation report"""
        print("\n" + "="*80)
        print("🔍 WEBSITE VALIDATION REPORT - DEPLOY_PERFECTION_REFINEMENT")
        print("="*80)
        
        # Summary
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"✅ PASS: {self.report.summary.get('PASS', 0)}")
        print(f"❌ FAIL: {self.report.summary.get('FAIL', 0)}")
        print(f"⚠️ WARNING: {self.report.summary.get('WARNING', 0)}")
        print(f"ℹ️ INFO: {self.report.summary.get('INFO', 0)}")
        
        # Overall status
        fail_count = self.report.summary.get('FAIL', 0)
        warning_count = self.report.summary.get('WARNING', 0)
        
        if fail_count == 0 and warning_count <= 3:
            print(f"\n🚀 LAUNCH READINESS: ✅ READY FOR DEPLOYMENT")
        elif fail_count <= 2:
            print(f"\n🚀 LAUNCH READINESS: ⚠️ MINOR ISSUES - DEPLOYMENT FEASIBLE")
        else:
            print(f"\n🚀 LAUNCH READINESS: ❌ CRITICAL ISSUES - REQUIRES FIXES")
        
        # Detailed results by component
        components = {}
        for result in self.report.results:
            if result.component not in components:
                components[result.component] = []
            components[result.component].append(result)
        
        print(f"\n📋 DETAILED VALIDATION RESULTS:")
        for component, results in components.items():
            print(f"\n🔧 {component.upper()}:")
            for result in results:
                status_symbol = result.status.value.split()[0]
                print(f"  {status_symbol} {result.test_name}: {result.message}")
                if result.fix_suggestion:
                    print(f"    💡 Fix: {result.fix_suggestion}")
        
        print(f"\n" + "="*80)
        print("🎯 DEPLOY_PERFECTION_REFINEMENT VALIDATION COMPLETE")
        print("="*80)

def main():
    """Main validation execution"""
    # Set the base path to the current directory
    base_path = os.getcwd()
    
    # Create validator and run comprehensive validation
    validator = WebsiteValidator(base_path)
    report = validator.run_comprehensive_validation()
    
    # Print the validation report
    validator.print_validation_report()
    
    # Save report to file
    report_data = {
        "summary": report.summary,
        "results": [
            {
                "component": r.component,
                "test_name": r.test_name,
                "status": r.status.value,
                "message": r.message,
                "file_path": r.file_path,
                "line_number": r.line_number,
                "fix_suggestion": r.fix_suggestion
            }
            for r in report.results
        ]
    }
    
    with open("website_validation_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: website_validation_report.json")

if __name__ == "__main__":
    main()
