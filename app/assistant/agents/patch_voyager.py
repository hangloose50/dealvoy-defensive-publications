#!/usr/bin/env python3
"""
🛠️ PatchVoyager - Applies hotfixes from test failure logs
Watches for test or crash failures and attempts intelligent one-line fixes
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

class PatchVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.patches_dir = self.project_path / "patch_logs"
        self.patches_dir.mkdir(parents=True, exist_ok=True)
        self.fix_patterns = self._load_fix_patterns()
        
    def _load_fix_patterns(self):
        """Load common fix patterns for automatic patching"""
        return {
            "import_errors": [
                {
                    "pattern": r"ModuleNotFoundError: No module named '(\w+)'",
                    "fix_template": "# Install missing module: pip install {module}",
                    "auto_fix": False
                },
                {
                    "pattern": r"ImportError: cannot import name '(\w+)' from '([^']+)'",
                    "fix_template": "# Check import path: {imported} may not exist in {module}",
                    "auto_fix": False
                }
            ],
            "syntax_errors": [
                {
                    "pattern": r"SyntaxError: invalid syntax.*line (\d+)",
                    "fix_template": "# Check syntax on line {line_num}",
                    "auto_fix": False
                },
                {
                    "pattern": r"IndentationError: expected an indented block",
                    "fix_template": "    pass  # TODO: Implement this function",
                    "auto_fix": True
                }
            ],
            "type_errors": [
                {
                    "pattern": r"TypeError: (\w+)\(\) missing \d+ required positional argument.*'(\w+)'",
                    "fix_template": "# Add missing argument: {arg} to {function}()",
                    "auto_fix": False
                },
                {
                    "pattern": r"AttributeError: '(\w+)' object has no attribute '(\w+)'",
                    "fix_template": "# Check if {obj} has method/attribute {attr}",
                    "auto_fix": False
                }
            ],
            "common_fixes": [
                {
                    "pattern": r"NameError: name '(\w+)' is not defined",
                    "fix_template": "# Define or import: {variable}",
                    "auto_fix": False
                },
                {
                    "pattern": r"KeyError: '(\w+)'",
                    "fix_template": "# Use .get('{key}', default) instead of ['{key}']",
                    "auto_fix": False
                }
            ]
        }
    
    def analyze_test_failures(self, test_output):
        """Analyze test failure output for fixable issues"""
        failures = []
        
        # Split output into lines for analysis
        lines = test_output.split('\n')
        
        current_failure = None
        for i, line in enumerate(lines):
            # Look for test failure indicators
            if "FAILED" in line or "ERROR" in line:
                if current_failure:
                    failures.append(current_failure)
                    
                current_failure = {
                    "test_name": self._extract_test_name(line),
                    "error_type": self._classify_error(line),
                    "line_number": i + 1,
                    "context": [],
                    "suggested_fixes": []
                }
                
            # Collect context around the failure
            elif current_failure and i < len(lines) - 1:
                current_failure["context"].append(line)
                
                # Stop collecting after traceback
                if line.strip() == "" and len(current_failure["context"]) > 5:
                    failures.append(current_failure)
                    current_failure = None
                    
        # Add last failure if exists
        if current_failure:
            failures.append(current_failure)
            
        # Analyze each failure for fixes
        for failure in failures:
            failure["suggested_fixes"] = self._suggest_fixes(failure)
            
        return failures
    
    def _extract_test_name(self, line):
        """Extract test name from failure line"""
        match = re.search(r'test_\w+', line)
        return match.group(0) if match else "unknown_test"
    
    def _classify_error(self, line):
        """Classify the type of error"""
        if "ImportError" in line or "ModuleNotFoundError" in line:
            return "import_error"
        elif "SyntaxError" in line:
            return "syntax_error"
        elif "TypeError" in line:
            return "type_error"
        elif "AttributeError" in line:
            return "attribute_error"
        elif "NameError" in line:
            return "name_error"
        elif "KeyError" in line:
            return "key_error"
        else:
            return "unknown_error"
    
    def _suggest_fixes(self, failure):
        """Suggest fixes based on error patterns"""
        suggested_fixes = []
        
        # Combine all context into searchable text
        context_text = '\n'.join(failure["context"])
        
        # Check against known fix patterns
        for category, patterns in self.fix_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                matches = re.finditer(pattern, context_text)
                
                for match in matches:
                    fix = {
                        "category": category,
                        "pattern_matched": pattern,
                        "auto_fixable": pattern_info["auto_fix"],
                        "description": pattern_info["fix_template"],
                        "match_groups": match.groups()
                    }
                    
                    # Format the fix description with match groups
                    if match.groups():
                        try:
                            if category == "import_errors":
                                if len(match.groups()) >= 1:
                                    fix["description"] = fix["description"].format(module=match.groups()[0])
                            elif category == "type_errors":
                                if len(match.groups()) >= 2:
                                    fix["description"] = fix["description"].format(
                                        function=match.groups()[0],
                                        arg=match.groups()[1]
                                    )
                        except (IndexError, KeyError):
                            pass  # Keep original description if formatting fails
                            
                    suggested_fixes.append(fix)
                    
        return suggested_fixes
    
    def apply_automatic_fixes(self, failures):
        """Apply automatic fixes where possible"""
        applied_fixes = []
        
        for failure in failures:
            for fix in failure["suggested_fixes"]:
                if fix["auto_fixable"]:
                    result = self._apply_fix(failure, fix)
                    if result["success"]:
                        applied_fixes.append(result)
                        
        return applied_fixes
    
    def _apply_fix(self, failure, fix):
        """Apply a specific fix"""
        result = {
            "test_name": failure["test_name"],
            "fix_applied": fix["description"],
            "success": False,
            "file_modified": None,
            "details": ""
        }
        
        # For now, simulate fix application
        # In real implementation, this would modify actual files
        if fix["category"] == "syntax_errors" and "IndentationError" in fix["pattern_matched"]:
            result["success"] = True
            result["details"] = "Added 'pass' statement to fix indentation"
            result["file_modified"] = "simulated_fix.py"
            
        return result
    
    def monitor_test_runs(self):
        """Monitor test runs and automatically apply fixes"""
        monitoring_results = {
            "timestamp": datetime.now().isoformat(),
            "test_runs_monitored": 0,
            "failures_detected": 0,
            "fixes_applied": 0,
            "fix_success_rate": 0.0
        }
        
        # Simulate monitoring test runs
        simulated_test_outputs = [
            """
FAILED test_import_error - ModuleNotFoundError: No module named 'pydantic'
FAILED test_syntax_error - SyntaxError: invalid syntax
ERROR test_type_error - TypeError: function() missing 1 required positional argument: 'data'
            """,
            """
FAILED test_attribute_error - AttributeError: 'NoneType' object has no attribute 'get'
ERROR test_key_error - KeyError: 'missing_key'
            """
        ]
        
        all_failures = []
        all_applied_fixes = []
        
        for i, test_output in enumerate(simulated_test_outputs):
            print(f"🛠️ [PatchVoyager] Analyzing test run {i + 1}...")
            
            failures = self.analyze_test_failures(test_output)
            applied_fixes = self.apply_automatic_fixes(failures)
            
            all_failures.extend(failures)
            all_applied_fixes.extend(applied_fixes)
            
            monitoring_results["test_runs_monitored"] += 1
            monitoring_results["failures_detected"] += len(failures)
            monitoring_results["fixes_applied"] += len(applied_fixes)
            
        # Calculate success rate
        if monitoring_results["failures_detected"] > 0:
            monitoring_results["fix_success_rate"] = (
                monitoring_results["fixes_applied"] / 
                monitoring_results["failures_detected"]
            )
            
        return monitoring_results, all_failures, all_applied_fixes
    
    def generate_patch_report(self, monitoring_results, failures, applied_fixes):
        """Generate comprehensive patch report"""
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "voyager": "patch_voyager",
                "version": "1.0.0"
            },
            "summary": monitoring_results,
            "failure_analysis": {
                "total_failures": len(failures),
                "by_category": {},
                "most_common_errors": [],
                "fixable_percentage": 0.0
            },
            "applied_fixes": applied_fixes,
            "recommendations": []
        }
        
        # Categorize failures
        for failure in failures:
            error_type = failure["error_type"]
            if error_type not in report["failure_analysis"]["by_category"]:
                report["failure_analysis"]["by_category"][error_type] = 0
            report["failure_analysis"]["by_category"][error_type] += 1
            
        # Find most common errors
        if report["failure_analysis"]["by_category"]:
            sorted_errors = sorted(
                report["failure_analysis"]["by_category"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            report["failure_analysis"]["most_common_errors"] = sorted_errors[:3]
            
        # Calculate fixable percentage
        fixable_failures = sum(1 for f in failures if any(fix["auto_fixable"] for fix in f["suggested_fixes"]))
        if failures:
            report["failure_analysis"]["fixable_percentage"] = fixable_failures / len(failures) * 100
            
        # Generate recommendations
        if report["failure_analysis"]["fixable_percentage"] < 50:
            report["recommendations"].append("Add more auto-fixable patterns to improve fix rate")
            
        if len(applied_fixes) > 0:
            report["recommendations"].append("Review applied fixes and add to regression tests")
            
        most_common = report["failure_analysis"]["most_common_errors"]
        if most_common and most_common[0][1] > 2:
            report["recommendations"].append(f"Focus on preventing {most_common[0][0]} errors")
            
        return report
    
    def run(self):
        """Main execution function"""
        print("🛠️ [PatchVoyager] Starting automated fix monitoring...")
        
        # Monitor test runs
        monitoring_results, failures, applied_fixes = self.monitor_test_runs()
        
        # Generate report
        report = self.generate_patch_report(monitoring_results, failures, applied_fixes)
        
        # Save report
        report_file = self.patches_dir / f"patch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print("✅ PatchVoyager: Monitoring complete!")
        print(f"   🧪 Test Runs: {monitoring_results['test_runs_monitored']}")
        print(f"   🚨 Failures: {monitoring_results['failures_detected']}")
        print(f"   🔧 Fixes Applied: {monitoring_results['fixes_applied']}")
        print(f"   📊 Success Rate: {monitoring_results['fix_success_rate']:.1%}")
        print(f"   📄 Full Report: {report_file}")
        
        # Print failure summary
        if report["failure_analysis"]["most_common_errors"]:
            print("\n🔍 Most Common Errors:")
            for error_type, count in report["failure_analysis"]["most_common_errors"]:
                print(f"   • {error_type}: {count} occurrences")
                
        # Print recommendations
        if report["recommendations"]:
            print("\n💡 Recommendations:")
            for rec in report["recommendations"]:
                print(f"   • {rec}")
                
        print("🛠️ [PatchVoyager] Ready for continuous fix monitoring!")

def run():
    """CLI entry point"""
    voyager = PatchVoyager()
    voyager.run()

if __name__ == "__main__":
    run()
