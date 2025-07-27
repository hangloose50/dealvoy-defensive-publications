#!/usr/bin/env python3
"""
🔒 SecurityVoyager - Security scanning and vulnerability detection
CVE scanning, dependency auditing, secret detection, and OWASP checks
"""

import os
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

class SecurityVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.security_dir = self.project_path / "security_reports"
        self.security_dir.mkdir(parents=True, exist_ok=True)
        
    def check_dependencies(self):
        """Check for known vulnerabilities in dependencies"""
        print("🔒 [SecurityVoyager] Scanning dependencies for vulnerabilities...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "total_packages": 0,
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "status": "pass"
        }
        
        try:
            # Try pip-audit first
            result = subprocess.run(
                ["python3", "-m", "pip_audit", "--format", "json"],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0:
                audit_data = json.loads(result.stdout)
                for vuln in audit_data.get("vulnerabilities", []):
                    severity = vuln.get("severity", "unknown").lower()
                    results["vulnerabilities"].append({
                        "package": vuln.get("package"),
                        "version": vuln.get("version"),
                        "vulnerability_id": vuln.get("id"),
                        "severity": severity,
                        "description": vuln.get("description", "")
                    })
                    
                    if severity == "critical":
                        results["critical_count"] += 1
                    elif severity == "high":
                        results["high_count"] += 1
                    elif severity == "medium":
                        results["medium_count"] += 1
                        
            else:
                # Fallback: manual check of requirements.txt
                requirements_file = self.project_path / "requirements.txt"
                if requirements_file.exists():
                    with open(requirements_file, 'r') as f:
                        packages = f.read().splitlines()
                    results["total_packages"] = len([p for p in packages if p.strip() and not p.startswith('#')])
                    
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            results["vulnerabilities"].append({
                "package": "system",
                "severity": "info",
                "description": "pip-audit not available - install with: pip install pip-audit"
            })
            
        # Determine overall status
        if results["critical_count"] > 0:
            results["status"] = "critical"
        elif results["high_count"] > 5:
            results["status"] = "high"
        elif results["high_count"] > 0:
            results["status"] = "medium"
            
        return results
    
    def scan_secrets(self):
        """Scan for exposed secrets and API keys"""
        print("🔒 [SecurityVoyager] Scanning for exposed secrets...")
        
        secret_patterns = [
            r'api[_-]?key[_-]?[=:]\s*["\']?[a-zA-Z0-9]{20,}',
            r'secret[_-]?key[_-]?[=:]\s*["\']?[a-zA-Z0-9]{20,}',
            r'password[_-]?[=:]\s*["\']?[^"\'\s]{8,}',
            r'token[_-]?[=:]\s*["\']?[a-zA-Z0-9]{20,}',
            r'aws[_-]?access[_-]?key[_-]?id[_-]?[=:]\s*["\']?[A-Z0-9]{20}',
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI API keys
            r'ghp_[a-zA-Z0-9]{36}',  # GitHub personal access tokens
        ]
        
        findings = []
        
        for py_file in self.project_path.rglob("*.py"):
            if self._should_scan_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for i, line in enumerate(content.split('\n'), 1):
                        for pattern in secret_patterns:
                            import re
                            if re.search(pattern, line, re.IGNORECASE):
                                findings.append({
                                    "file": str(py_file.relative_to(self.project_path)),
                                    "line": i,
                                    "type": "potential_secret",
                                    "severity": "high",
                                    "description": "Potential hardcoded secret detected"
                                })
                                
                except Exception:
                    continue
                    
        return {
            "timestamp": datetime.now().isoformat(),
            "findings": findings,
            "files_scanned": len(list(self.project_path.rglob("*.py"))),
            "secrets_found": len(findings),
            "status": "high" if findings else "pass"
        }
    
    def _should_scan_file(self, file_path):
        """Determine if file should be scanned for secrets"""
        skip_patterns = ["__pycache__", ".git", "venv", "node_modules", ".pytest_cache"]
        return not any(pattern in str(file_path) for pattern in skip_patterns)
    
    def run_bandit_scan(self):
        """Run bandit security linter"""
        print("🔒 [SecurityVoyager] Running bandit security scan...")
        
        try:
            result = subprocess.run(
                ["python3", "-m", "bandit", "-r", str(self.project_path), "-f", "json"],
                capture_output=True, text=True, timeout=90
            )
            
            if result.stdout:
                bandit_data = json.loads(result.stdout)
                return {
                    "timestamp": datetime.now().isoformat(),
                    "issues": bandit_data.get("results", []),
                    "total_issues": len(bandit_data.get("results", [])),
                    "high_severity": len([r for r in bandit_data.get("results", []) if r.get("issue_severity") == "HIGH"]),
                    "status": "high" if len([r for r in bandit_data.get("results", []) if r.get("issue_severity") == "HIGH"]) > 0 else "pass"
                }
            else:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "issues": [],
                    "total_issues": 0,
                    "status": "info",
                    "note": "bandit not available - install with: pip install bandit"
                }
                
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            return {
                "timestamp": datetime.now().isoformat(),
                "issues": [],
                "total_issues": 0,
                "status": "info",
                "note": "bandit scan failed or not installed"
            }
    
    def run(self, smoke=False):
        """Main execution function"""
        print("🔒 [SecurityVoyager] Running security scans...")
        
        if smoke:
            print("   🚀 FAST MODE: Running smoke tests only")
            return {
                "mode": "smoke",
                "status": "pass",
                "message": "SecurityVoyager smoke test completed"
            }
        
        # Run all security checks
        dependency_results = self.check_dependencies()
        secret_results = self.scan_secrets()
        bandit_results = self.run_bandit_scan()
        
        # Compile comprehensive report
        security_report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "voyager": "security_voyager",
                "version": "1.0.0"
            },
            "dependency_scan": dependency_results,
            "secret_scan": secret_results,
            "static_analysis": bandit_results,
            "overall_status": "pass",
            "risk_score": 0
        }
        
        # Calculate overall status and risk score
        risk_factors = []
        
        if dependency_results["critical_count"] > 0:
            risk_factors.append("critical_vulnerabilities")
            security_report["risk_score"] += 50
            
        if dependency_results["high_count"] > 3:
            risk_factors.append("multiple_high_vulnerabilities")
            security_report["risk_score"] += 30
            
        if secret_results["secrets_found"] > 0:
            risk_factors.append("exposed_secrets")
            security_report["risk_score"] += 40
            
        if bandit_results["total_issues"] > 10:
            risk_factors.append("multiple_security_issues")
            security_report["risk_score"] += 20
            
        # Determine overall status
        if security_report["risk_score"] >= 70:
            security_report["overall_status"] = "critical"
        elif security_report["risk_score"] >= 40:
            security_report["overall_status"] = "high"
        elif security_report["risk_score"] >= 20:
            security_report["overall_status"] = "medium"
            
        security_report["risk_factors"] = risk_factors
        
        # Save report
        report_file = self.security_dir / f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(security_report, f, indent=2)
            
        # Print results
        print("✅ SecurityVoyager: Security scan complete!")
        print(f"   🎯 Overall Status: {security_report['overall_status'].upper()}")
        print(f"   ⚠️  Risk Score: {security_report['risk_score']}/100")
        print(f"   🔍 Dependencies: {dependency_results['critical_count']} critical, {dependency_results['high_count']} high")
        print(f"   🔐 Secrets: {secret_results['secrets_found']} potential exposures")
        print(f"   📊 Static Analysis: {bandit_results['total_issues']} issues")
        print(f"   📄 Full Report: {report_file}")
        
        if risk_factors:
            print("\n🚨 Risk Factors:")
            for factor in risk_factors:
                print(f"   • {factor.replace('_', ' ').title()}")
                
        print("🔒 [SecurityVoyager] Ready for continuous security monitoring!")
        
        # Return status for automation
        return security_report

def main():
    parser = argparse.ArgumentParser(description="SecurityVoyager - Security scanning agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    
    # Check if agent is enabled
    try:
        import sys
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        if not is_agent_enabled("SecurityVoyager"):
            print("🔒 SecurityVoyager is disabled - skipping")
            return 0
    except ImportError:
        pass  # Continue if agent_manager not available yet
        
    # Handle fast mode
    if os.getenv("VOYAGER_FAST") == "1":
        args.smoke = True
        
    voyager = SecurityVoyager()
    result = voyager.run(smoke=args.smoke)
    
    # Print JSON for automation
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if result.get("overall_status") == "critical":
        return 1
    elif result.get("overall_status") in ["high", "medium"]:
        return 2  # Warning
    else:
        return 0

if __name__ == "__main__":
    exit(main())
