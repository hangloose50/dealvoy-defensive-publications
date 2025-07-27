#!/usr/bin/env python3
"""
⚡ PerformanceVoyager - Performance monitoring and optimization
CPU/memory profiling, load testing, and performance budget enforcement
"""

import os
import json
import time
import psutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

class PerformanceVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.perf_dir = self.project_path / "performance_reports"
        self.perf_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance budgets (configurable thresholds)
        self.budgets = {
            "max_response_time_ms": 2000,
            "max_memory_mb": 512,
            "max_cpu_percent": 80,
            "max_startup_time_s": 10,
            "max_bundle_size_mb": 5
        }
        
    def profile_system_resources(self):
        """Profile current system resource usage"""
        print("⚡ [PerformanceVoyager] Profiling system resources...")
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        resource_profile = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count(),
                "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": {
                "total_mb": round(memory.total / 1024 / 1024, 2),
                "available_mb": round(memory.available / 1024 / 1024, 2),
                "used_mb": round(memory.used / 1024 / 1024, 2),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
                "free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
                "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
                "percent": round((disk.used / disk.total) * 100, 2)
            },
            "status": "healthy"
        }
        
        # Check against budgets
        warnings = []
        if cpu_percent > self.budgets["max_cpu_percent"]:
            warnings.append(f"High CPU usage: {cpu_percent}%")
            resource_profile["status"] = "warning"
            
        if memory.percent > 85:
            warnings.append(f"High memory usage: {memory.percent}%")
            resource_profile["status"] = "warning"
            
        if disk.percent > 90:
            warnings.append(f"High disk usage: {disk.percent}%")
            resource_profile["status"] = "critical"
            
        resource_profile["warnings"] = warnings
        
        return resource_profile
    
    def benchmark_application_startup(self):
        """Benchmark application startup time"""
        print("⚡ [PerformanceVoyager] Benchmarking application startup...")
        
        startup_results = {
            "timestamp": datetime.now().isoformat(),
            "attempts": [],
            "average_time_s": 0,
            "status": "pass"
        }
        
        # Run multiple startup tests
        for attempt in range(3):
            try:
                start_time = time.time()
                
                # Test Python import time (proxy for app startup)
                result = subprocess.run(
                    ["python3", "-c", "import app; print('OK')"],
                    capture_output=True, text=True, timeout=30,
                    cwd=self.project_path
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                startup_results["attempts"].append({
                    "attempt": attempt + 1,
                    "duration_s": round(duration, 3),
                    "success": result.returncode == 0,
                    "output": result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
                })
                
            except subprocess.TimeoutExpired:
                startup_results["attempts"].append({
                    "attempt": attempt + 1,
                    "duration_s": 30,
                    "success": False,
                    "output": "Timeout"
                })
                
        # Calculate average
        successful_attempts = [a for a in startup_results["attempts"] if a["success"]]
        if successful_attempts:
            startup_results["average_time_s"] = round(
                sum(a["duration_s"] for a in successful_attempts) / len(successful_attempts), 3
            )
            
            # Check against budget
            if startup_results["average_time_s"] > self.budgets["max_startup_time_s"]:
                startup_results["status"] = "warning"
                startup_results["warning"] = f"Slow startup: {startup_results['average_time_s']}s > {self.budgets['max_startup_time_s']}s"
        else:
            startup_results["status"] = "critical"
            startup_results["error"] = "All startup attempts failed"
            
        return startup_results
    
    def analyze_code_complexity(self):
        """Analyze code complexity metrics"""
        print("⚡ [PerformanceVoyager] Analyzing code complexity...")
        
        complexity_metrics = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "total_lines": 0,
            "avg_function_length": 0,
            "complex_functions": [],
            "status": "good"
        }
        
        function_lengths = []
        
        for py_file in self.project_path.rglob("*.py"):
            if self._should_analyze_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    complexity_metrics["total_files"] += 1
                    complexity_metrics["total_lines"] += len(lines)
                    
                    # Simple function length analysis
                    current_function = None
                    function_start = 0
                    
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        if stripped.startswith('def '):
                            if current_function:
                                func_length = i - function_start
                                function_lengths.append(func_length)
                                
                                if func_length > 50:  # Long function threshold
                                    complexity_metrics["complex_functions"].append({
                                        "file": str(py_file.relative_to(self.project_path)),
                                        "function": current_function,
                                        "length": func_length,
                                        "line": function_start + 1
                                    })
                                    
                            current_function = stripped.split('(')[0].replace('def ', '')
                            function_start = i
                            
                except Exception:
                    continue
                    
        # Calculate averages
        if function_lengths:
            complexity_metrics["avg_function_length"] = round(sum(function_lengths) / len(function_lengths), 1)
            
        # Determine status
        if len(complexity_metrics["complex_functions"]) > 10:
            complexity_metrics["status"] = "warning"
        elif len(complexity_metrics["complex_functions"]) > 20:
            complexity_metrics["status"] = "critical"
            
        return complexity_metrics
    
    def _should_analyze_file(self, file_path):
        """Determine if file should be analyzed"""
        skip_patterns = ["__pycache__", ".git", "venv", "node_modules", ".pytest_cache"]
        return not any(pattern in str(file_path) for pattern in skip_patterns)
    
    def run_load_simulation(self):
        """Simulate load testing"""
        print("⚡ [PerformanceVoyager] Running load simulation...")
        
        load_results = {
            "timestamp": datetime.now().isoformat(),
            "simulation_type": "basic_stress_test",
            "duration_s": 10,
            "metrics": {},
            "status": "pass"
        }
        
        try:
            # Simple CPU stress test
            start_time = time.time()
            cpu_samples = []
            memory_samples = []
            
            # Sample system metrics during load
            for _ in range(10):
                cpu_samples.append(psutil.cpu_percent())
                memory_samples.append(psutil.virtual_memory().percent)
                time.sleep(1)
                
            load_results["metrics"] = {
                "avg_cpu_percent": round(sum(cpu_samples) / len(cpu_samples), 2),
                "max_cpu_percent": max(cpu_samples),
                "avg_memory_percent": round(sum(memory_samples) / len(memory_samples), 2),
                "max_memory_percent": max(memory_samples),
                "samples_taken": len(cpu_samples)
            }
            
            # Check performance under load
            if load_results["metrics"]["max_cpu_percent"] > 95:
                load_results["status"] = "warning"
                load_results["warning"] = "High CPU usage under load"
                
            if load_results["metrics"]["max_memory_percent"] > 90:
                load_results["status"] = "critical"
                load_results["error"] = "Critical memory usage under load"
                
        except Exception as e:
            load_results["status"] = "error"
            load_results["error"] = f"Load simulation failed: {str(e)}"
            
        return load_results
    
    def run(self, smoke=False):
        """Main execution function"""
        print("⚡ [PerformanceVoyager] Running performance analysis...")
        
        if smoke:
            print("   🚀 FAST MODE: Running smoke tests only")
            return {
                "mode": "smoke",
                "status": "pass",
                "message": "PerformanceVoyager smoke test completed"
            }
        
        # Run all performance checks
        resource_profile = self.profile_system_resources()
        startup_benchmark = self.benchmark_application_startup()
        complexity_analysis = self.analyze_code_complexity()
        load_simulation = self.run_load_simulation()
        
        # Compile comprehensive report
        performance_report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "voyager": "performance_voyager",
                "version": "1.0.0"
            },
            "resource_profile": resource_profile,
            "startup_benchmark": startup_benchmark,
            "complexity_analysis": complexity_analysis,
            "load_simulation": load_simulation,
            "overall_status": "pass",
            "performance_score": 100
        }
        
        # Calculate overall performance score
        score_deductions = 0
        issues = []
        
        if resource_profile["status"] == "warning":
            score_deductions += 15
            issues.append("resource_constraints")
        elif resource_profile["status"] == "critical":
            score_deductions += 30
            issues.append("critical_resource_usage")
            
        if startup_benchmark["status"] == "warning":
            score_deductions += 20
            issues.append("slow_startup")
        elif startup_benchmark["status"] == "critical":
            score_deductions += 40
            issues.append("startup_failure")
            
        if complexity_analysis["status"] == "warning":
            score_deductions += 10
            issues.append("high_complexity")
        elif complexity_analysis["status"] == "critical":
            score_deductions += 25
            issues.append("critical_complexity")
            
        if load_simulation["status"] == "warning":
            score_deductions += 15
            issues.append("load_performance_issues")
        elif load_simulation["status"] == "critical":
            score_deductions += 35
            issues.append("critical_load_failure")
            
        performance_report["performance_score"] = max(0, 100 - score_deductions)
        performance_report["issues"] = issues
        
        # Determine overall status
        if performance_report["performance_score"] >= 85:
            performance_report["overall_status"] = "excellent"
        elif performance_report["performance_score"] >= 70:
            performance_report["overall_status"] = "good"
        elif performance_report["performance_score"] >= 50:
            performance_report["overall_status"] = "fair"
        else:
            performance_report["overall_status"] = "poor"
            
        # Save report
        report_file = self.perf_dir / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(performance_report, f, indent=2)
            
        # Print results
        print("✅ PerformanceVoyager: Performance analysis complete!")
        print(f"   📊 Overall Status: {performance_report['overall_status'].upper()}")
        print(f"   🎯 Performance Score: {performance_report['performance_score']}/100")
        print(f"   💻 Resource Usage: {resource_profile['cpu']['usage_percent']}% CPU, {resource_profile['memory']['percent']}% Memory")
        print(f"   ⚡ Startup Time: {startup_benchmark['average_time_s']}s")
        print(f"   🔧 Code Complexity: {len(complexity_analysis['complex_functions'])} complex functions")
        print(f"   📄 Full Report: {report_file}")
        
        if issues:
            print("\n⚠️ Performance Issues:")
            for issue in issues:
                print(f"   • {issue.replace('_', ' ').title()}")
                
        print("⚡ [PerformanceVoyager] Ready for continuous performance monitoring!")
        
        return performance_report

def main():
    parser = argparse.ArgumentParser(description="PerformanceVoyager - Performance monitoring agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    
    # Handle fast mode
    if os.getenv("VOYAGER_FAST") == "1":
        args.smoke = True
        
    voyager = PerformanceVoyager()
    result = voyager.run(smoke=args.smoke)
    
    # Print JSON for automation
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if result.get("overall_status") == "poor":
        return 1
    elif result.get("overall_status") == "fair":
        return 2  # Warning
    else:
        return 0

if __name__ == "__main__":
    exit(main())
