#!/usr/bin/env python3
"""
📡 FeedbackVoyager - Gathers live UX/ML feedback from user interactions
Observes user flow and logs metrics for continuous improvement
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

class FeedbackVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.feedback_dir = self.project_path / "feedback_data"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = {}
        
    def initialize_metrics_tracking(self):
        """Initialize metrics collection system"""
        metrics_config = {
            "user_interactions": {
                "scan_attempts": 0,
                "successful_scans": 0,
                "scan_accuracy": 0.0,
                "average_scan_time": 0.0
            },
            "performance_metrics": {
                "ocr_processing_time": [],
                "price_lookup_time": [],
                "total_request_time": [],
                "error_rates": {}
            },
            "user_behavior": {
                "session_duration": [],
                "pages_visited": [],
                "feature_usage": {},
                "drop_off_points": {}
            },
            "business_metrics": {
                "deals_found": 0,
                "deals_saved": 0,
                "conversion_rate": 0.0,
                "user_satisfaction": 0.0
            }
        }
        
        self.metrics = metrics_config
        return metrics_config
    
    def track_user_interaction(self, interaction_type, data):
        """Track specific user interaction"""
        timestamp = datetime.now()
        
        interaction_log = {
            "timestamp": timestamp.isoformat(),
            "type": interaction_type,
            "data": data,
            "session_id": data.get("session_id", "unknown")
        }
        
        # Update relevant metrics
        if interaction_type == "scan_product":
            self.metrics["user_interactions"]["scan_attempts"] += 1
            
            if data.get("success", False):
                self.metrics["user_interactions"]["successful_scans"] += 1
                
            processing_time = data.get("processing_time", 0)
            if processing_time > 0:
                current_times = self.metrics["performance_metrics"]["ocr_processing_time"]
                current_times.append(processing_time)
                self.metrics["user_interactions"]["average_scan_time"] = sum(current_times) / len(current_times)
                
        elif interaction_type == "price_lookup":
            lookup_time = data.get("lookup_time", 0)
            if lookup_time > 0:
                self.metrics["performance_metrics"]["price_lookup_time"].append(lookup_time)
                
        elif interaction_type == "save_deal":
            self.metrics["business_metrics"]["deals_saved"] += 1
            
        elif interaction_type == "error":
            error_type = data.get("error_type", "unknown")
            if error_type not in self.metrics["performance_metrics"]["error_rates"]:
                self.metrics["performance_metrics"]["error_rates"][error_type] = 0
            self.metrics["performance_metrics"]["error_rates"][error_type] += 1
            
        # Log interaction
        self._log_interaction(interaction_log)
        
        return interaction_log
    
    def _log_interaction(self, interaction_log):
        """Log interaction to file"""
        log_file = self.feedback_dir / f"interactions_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(interaction_log) + '\n')
    
    def analyze_user_patterns(self):
        """Analyze user behavior patterns"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "patterns": {},
            "insights": [],
            "recommendations": []
        }
        
        # Calculate key metrics
        scan_success_rate = 0
        if self.metrics["user_interactions"]["scan_attempts"] > 0:
            scan_success_rate = (
                self.metrics["user_interactions"]["successful_scans"] /
                self.metrics["user_interactions"]["scan_attempts"]
            )
            
        analysis["patterns"]["scan_success_rate"] = scan_success_rate
        analysis["patterns"]["average_processing_time"] = self.metrics["user_interactions"]["average_scan_time"]
        
        # Generate insights
        if scan_success_rate < 0.7:
            analysis["insights"].append("Low scan success rate detected")
            analysis["recommendations"].append("Improve OCR accuracy or user guidance")
            
        if self.metrics["user_interactions"]["average_scan_time"] > 5.0:
            analysis["insights"].append("Slow processing times affecting UX")
            analysis["recommendations"].append("Optimize OCR processing pipeline")
            
        # Error analysis
        error_rates = self.metrics["performance_metrics"]["error_rates"]
        if error_rates:
            most_common_error = max(error_rates.items(), key=lambda x: x[1])
            analysis["insights"].append(f"Most common error: {most_common_error[0]}")
            analysis["recommendations"].append(f"Address {most_common_error[0]} error handling")
            
        return analysis
    
    def generate_ml_training_data(self):
        """Generate training data for ML model improvements"""
        training_data = {
            "timestamp": datetime.now().isoformat(),
            "scan_results": [],
            "user_corrections": [],
            "performance_labels": []
        }
        
        # Read interaction logs
        for log_file in self.feedback_dir.glob("interactions_*.jsonl"):
            with open(log_file, 'r') as f:
                for line in f:
                    interaction = json.loads(line.strip())
                    
                    if interaction["type"] == "scan_product":
                        # Extract features for ML training
                        scan_data = {
                            "image_quality": interaction["data"].get("image_quality", 0.5),
                            "processing_time": interaction["data"].get("processing_time", 0),
                            "confidence_score": interaction["data"].get("confidence", 0.5),
                            "success": interaction["data"].get("success", False),
                            "user_satisfaction": interaction["data"].get("user_rating", 0.5)
                        }
                        training_data["scan_results"].append(scan_data)
                        
                    elif interaction["type"] == "user_correction":
                        # User corrections help improve accuracy
                        correction_data = {
                            "original_result": interaction["data"].get("original", ""),
                            "corrected_result": interaction["data"].get("corrected", ""),
                            "correction_type": interaction["data"].get("type", "text")
                        }
                        training_data["user_corrections"].append(correction_data)
                        
        return training_data
    
    def create_performance_dashboard(self):
        """Create performance dashboard data"""
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_scans": self.metrics["user_interactions"]["scan_attempts"],
                "success_rate": 0,
                "avg_processing_time": self.metrics["user_interactions"]["average_scan_time"],
                "deals_saved": self.metrics["business_metrics"]["deals_saved"]
            },
            "charts": {
                "processing_times": self.metrics["performance_metrics"]["ocr_processing_time"][-50:],
                "error_distribution": self.metrics["performance_metrics"]["error_rates"],
                "daily_usage": self._calculate_daily_usage()
            },
            "alerts": self._generate_performance_alerts()
        }
        
        # Calculate success rate
        if dashboard["summary"]["total_scans"] > 0:
            dashboard["summary"]["success_rate"] = (
                self.metrics["user_interactions"]["successful_scans"] /
                dashboard["summary"]["total_scans"]
            )
            
        return dashboard
    
    def _calculate_daily_usage(self):
        """Calculate daily usage statistics"""
        daily_stats = {}
        
        for log_file in self.feedback_dir.glob("interactions_*.jsonl"):
            date = log_file.stem.split('_')[1]
            daily_stats[date] = 0
            
            with open(log_file, 'r') as f:
                for line in f:
                    daily_stats[date] += 1
                    
        return daily_stats
    
    def _generate_performance_alerts(self):
        """Generate performance alerts"""
        alerts = []
        
        # Check processing time
        recent_times = self.metrics["performance_metrics"]["ocr_processing_time"][-10:]
        if recent_times and sum(recent_times) / len(recent_times) > 5.0:
            alerts.append({
                "type": "performance",
                "severity": "warning",
                "message": "Processing times above 5 seconds"
            })
            
        # Check error rates
        total_interactions = sum(self.metrics["performance_metrics"]["error_rates"].values())
        if total_interactions > 0:
            error_rate = total_interactions / self.metrics["user_interactions"]["scan_attempts"]
            if error_rate > 0.1:
                alerts.append({
                    "type": "reliability",
                    "severity": "critical",
                    "message": f"Error rate at {error_rate:.1%}"
                })
                
        return alerts
    
    def run(self):
        """Main execution function"""
        print("📡 [FeedbackVoyager] Initializing user feedback collection...")
        
        # Initialize metrics
        self.initialize_metrics_tracking()
        print("   Metrics tracking initialized")
        
        # Simulate some user interactions for demo
        demo_interactions = [
            {"type": "scan_product", "data": {"success": True, "processing_time": 2.1, "confidence": 0.85, "session_id": "demo1"}},
            {"type": "scan_product", "data": {"success": False, "processing_time": 1.8, "error_type": "low_quality", "session_id": "demo1"}},
            {"type": "price_lookup", "data": {"lookup_time": 1.5, "results_found": 3, "session_id": "demo1"}},
            {"type": "save_deal", "data": {"deal_value": 15.99, "savings": 5.00, "session_id": "demo1"}},
            {"type": "error", "data": {"error_type": "network_timeout", "context": "price_lookup", "session_id": "demo2"}}
        ]
        
        print("📡 [FeedbackVoyager] Processing demo user interactions...")
        for interaction in demo_interactions:
            self.track_user_interaction(interaction["type"], interaction["data"])
            time.sleep(0.1)  # Simulate real-time processing
            
        # Analyze patterns
        patterns = self.analyze_user_patterns()
        
        # Generate ML training data
        training_data = self.generate_ml_training_data()
        
        # Create dashboard
        dashboard = self.create_performance_dashboard()
        
        # Save results
        results_file = self.feedback_dir / f"feedback_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results = {
            "patterns": patterns,
            "training_data": training_data,
            "dashboard": dashboard,
            "raw_metrics": self.metrics
        }
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        print("✅ FeedbackVoyager: Analysis complete!")
        print(f"   📊 Success Rate: {dashboard['summary']['success_rate']:.1%}")
        print(f"   ⏱️  Avg Processing: {dashboard['summary']['avg_processing_time']:.1f}s")
        print(f"   💾 Deals Saved: {dashboard['summary']['deals_saved']}")
        print(f"   📄 Full Report: {results_file}")
        
        # Print insights
        if patterns["insights"]:
            print("\n🔍 Key Insights:")
            for insight in patterns["insights"]:
                print(f"   • {insight}")
                
        if patterns["recommendations"]:
            print("\n💡 Recommendations:")
            for rec in patterns["recommendations"]:
                print(f"   • {rec}")
                
        print("📡 [FeedbackVoyager] Ready for continuous feedback collection!")

def run():
    """CLI entry point"""
    voyager = FeedbackVoyager()
    voyager.run()

if __name__ == "__main__":
    run()
