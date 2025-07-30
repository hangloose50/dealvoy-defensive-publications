#!/usr/bin/env python3
"""
Scan Usage Tracking System
Handles scan logging, tier management, and automated upgrade prompts
"""

import json
import datetime
import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ScanLog:
    """Individual scan log entry"""
    id: str
    timestamp: str
    user_email: str
    user_tier: str
    agent_name: str
    scan_type: str
    outcome: str
    products_found: int
    processing_time_ms: int
    ip_address: str
    user_agent: str
    scan_parameters: Dict
    error_details: Optional[Dict] = None

@dataclass
class TierLimits:
    """Tier configuration and limits"""
    name: str
    scan_limit: int  # -1 for unlimited
    monthly_price: float
    features: List[str]

class ScanUsageTracker:
    """Main scan usage tracking and management system"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.scan_log_file = self.data_dir / "scan_usage_log.json"
        self.tier_config_file = self.data_dir / "tier_config.json"
        
        # Tier configurations
        self.tiers = {
            'starter': TierLimits('starter', 100, 12.0, ['5 AI agents', 'Basic support']),
            'pro': TierLimits('pro', 1000, 29.0, ['15 AI agents', 'Priority support', 'API access']),
            'enterprise': TierLimits('enterprise', 10000, 79.0, ['25 AI agents', 'Dedicated support', 'Custom integrations']),
            'titan': TierLimits('titan', -1, 159.0, ['35 AI agents', 'White-glove support', 'Unlimited everything']),
            'odyssey': TierLimits('odyssey', -1, 199.0, ['45 AI agents', 'Enterprise features', 'Custom development']),
            'vanguard': TierLimits('vanguard', -1, 399.0, ['Unlimited agents', 'Dedicated team', 'Custom solutions'])
        }
        
        self.load_data()
    
    def load_data(self):
        """Load existing scan data"""
        try:
            if self.scan_log_file.exists():
                with open(self.scan_log_file, 'r') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    "scan_logs": [],
                    "daily_summary": {},
                    "usage_alerts": [],
                    "revenue_projections": {}
                }
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = {"scan_logs": [], "daily_summary": {}, "usage_alerts": [], "revenue_projections": {}}
    
    def save_data(self):
        """Save scan data to file"""
        try:
            with open(self.scan_log_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def log_scan(self, user_email: str, user_tier: str, agent_name: str, 
                 scan_type: str, outcome: str, products_found: int,
                 processing_time_ms: int, ip_address: str, user_agent: str,
                 scan_parameters: Dict, error_details: Optional[Dict] = None) -> str:
        """Log a new scan"""
        
        scan_id = f"scan_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        scan_log = ScanLog(
            id=scan_id,
            timestamp=timestamp,
            user_email=user_email,
            user_tier=user_tier,
            agent_name=agent_name,
            scan_type=scan_type,
            outcome=outcome,
            products_found=products_found,
            processing_time_ms=processing_time_ms,
            ip_address=ip_address,
            user_agent=user_agent,
            scan_parameters=scan_parameters,
            error_details=error_details
        )
        
        self.data["scan_logs"].append(asdict(scan_log))
        self.save_data()
        
        # Check if user is approaching limits
        self.check_usage_alerts(user_email)
        
        return scan_id
    
    def get_user_scan_count(self, user_email: str, period: str = "monthly") -> int:
        """Get user's scan count for specified period"""
        today = datetime.date.today()
        
        if period == "monthly":
            start_date = today.replace(day=1)
        elif period == "daily":
            start_date = today
        elif period == "weekly":
            start_date = today - datetime.timedelta(days=7)
        else:
            start_date = datetime.date(1970, 1, 1)
        
        count = 0
        for log in self.data["scan_logs"]:
            if log["user_email"] == user_email and log["outcome"] == "success":
                log_date = datetime.datetime.fromisoformat(log["timestamp"].replace('Z', '+00:00')).date()
                if log_date >= start_date:
                    count += 1
        
        return count
    
    def check_usage_alerts(self, user_email: str) -> Optional[Dict]:
        """Check if user needs usage alerts"""
        # Get user's current tier and usage
        user_logs = [log for log in self.data["scan_logs"] if log["user_email"] == user_email]
        if not user_logs:
            return None
        
        latest_log = max(user_logs, key=lambda x: x["timestamp"])
        user_tier = latest_log["user_tier"]
        
        if user_tier not in self.tiers:
            return None
        
        tier_limit = self.tiers[user_tier].scan_limit
        
        # Unlimited tiers don't need alerts
        if tier_limit == -1:
            return None
        
        current_usage = self.get_user_scan_count(user_email, "monthly")
        usage_percentage = (current_usage / tier_limit) * 100
        
        alert = None
        if usage_percentage >= 100:
            alert = {
                "user_email": user_email,
                "tier": user_tier,
                "current_usage": current_usage,
                "usage_limit": tier_limit,
                "usage_percentage": usage_percentage,
                "alert_level": "critical",
                "alert_message": "Scan limit exceeded",
                "suggested_action": f"Upgrade required to continue scanning"
            }
        elif usage_percentage >= 90:
            alert = {
                "user_email": user_email,
                "tier": user_tier,
                "current_usage": current_usage,
                "usage_limit": tier_limit,
                "usage_percentage": usage_percentage,
                "alert_level": "critical",
                "alert_message": "User approaching scan limit",
                "suggested_action": f"Send upgrade notification"
            }
        elif usage_percentage >= 75:
            alert = {
                "user_email": user_email,
                "tier": user_tier,
                "current_usage": current_usage,
                "usage_limit": tier_limit,
                "usage_percentage": usage_percentage,
                "alert_level": "high",
                "alert_message": f"User at {usage_percentage:.1f}% of scan limit",
                "suggested_action": f"Show upgrade suggestion"
            }
        elif usage_percentage >= 50:
            alert = {
                "user_email": user_email,
                "tier": user_tier,
                "current_usage": current_usage,
                "usage_limit": tier_limit,
                "usage_percentage": usage_percentage,
                "alert_level": "medium",
                "alert_message": "User approaching scan limit",
                "suggested_action": f"Show upgrade suggestion"
            }
        
        if alert:
            # Update alerts in data
            existing_alerts = [a for a in self.data["usage_alerts"] if a["user_email"] != user_email]
            existing_alerts.append(alert)
            self.data["usage_alerts"] = existing_alerts
            self.save_data()
        
        return alert
    
    def get_upgrade_recommendation(self, user_tier: str) -> Optional[Dict]:
        """Get upgrade recommendation for current tier"""
        tier_order = ['starter', 'pro', 'enterprise', 'titan', 'odyssey', 'vanguard']
        
        if user_tier not in tier_order:
            return None
        
        current_index = tier_order.index(user_tier)
        if current_index >= len(tier_order) - 1:
            return None  # Already at highest tier
        
        next_tier_name = tier_order[current_index + 1]
        next_tier = self.tiers[next_tier_name]
        
        return {
            "current_tier": user_tier,
            "next_tier": next_tier_name,
            "new_limit": "Unlimited" if next_tier.scan_limit == -1 else next_tier.scan_limit,
            "price": f"${next_tier.monthly_price:.0f}/month",
            "benefits": next_tier.features
        }
    
    def can_user_scan(self, user_email: str) -> Tuple[bool, Optional[str]]:
        """Check if user can perform a scan"""
        # Get user's current tier
        user_logs = [log for log in self.data["scan_logs"] if log["user_email"] == user_email]
        if not user_logs:
            return True, None  # New user, allow scan
        
        latest_log = max(user_logs, key=lambda x: x["timestamp"])
        user_tier = latest_log["user_tier"]
        
        if user_tier not in self.tiers:
            return False, "Invalid user tier"
        
        tier_limit = self.tiers[user_tier].scan_limit
        
        # Unlimited tiers can always scan
        if tier_limit == -1:
            return True, None
        
        current_usage = self.get_user_scan_count(user_email, "monthly")
        
        if current_usage >= tier_limit:
            return False, f"Monthly scan limit of {tier_limit} exceeded. Please upgrade your plan."
        
        return True, None
    
    def generate_daily_summary(self, date: datetime.date = None) -> Dict:
        """Generate daily usage summary"""
        if date is None:
            date = datetime.date.today()
        
        date_str = date.isoformat()
        
        # Filter logs for the day
        day_logs = []
        for log in self.data["scan_logs"]:
            log_date = datetime.datetime.fromisoformat(log["timestamp"].replace('Z', '+00:00')).date()
            if log_date == date:
                day_logs.append(log)
        
        # Calculate summary stats
        total_scans = len(day_logs)
        successful_scans = len([log for log in day_logs if log["outcome"] == "success"])
        failed_scans = total_scans - successful_scans
        unique_users = len(set(log["user_email"] for log in day_logs))
        
        # Top agents
        agent_usage = {}
        for log in day_logs:
            agent = log["agent_name"]
            if agent not in agent_usage:
                agent_usage[agent] = {"count": 0, "successes": 0}
            agent_usage[agent]["count"] += 1
            if log["outcome"] == "success":
                agent_usage[agent]["successes"] += 1
        
        top_agents = []
        for agent, stats in sorted(agent_usage.items(), key=lambda x: x[1]["count"], reverse=True)[:5]:
            success_rate = (stats["successes"] / stats["count"]) * 100 if stats["count"] > 0 else 0
            top_agents.append({
                "name": agent,
                "usage_count": stats["count"],
                "success_rate": round(success_rate, 1)
            })
        
        # Tier usage
        tier_usage = {}
        for tier in self.tiers.keys():
            tier_logs = [log for log in day_logs if log["user_tier"] == tier]
            unique_tier_users = len(set(log["user_email"] for log in tier_logs))
            total_tier_scans = len(tier_logs)
            avg_scans = total_tier_scans / unique_tier_users if unique_tier_users > 0 else 0
            
            tier_usage[tier] = {
                "users": unique_tier_users,
                "total_scans": total_tier_scans,
                "avg_scans_per_user": round(avg_scans, 1),
                "users_near_limit": len([alert for alert in self.data["usage_alerts"] 
                                       if alert["tier"] == tier and alert["usage_percentage"] >= 75])
            }
        
        summary = {
            "date": date_str,
            "total_scans": total_scans,
            "successful_scans": successful_scans,
            "failed_scans": failed_scans,
            "unique_users": unique_users,
            "top_agents": top_agents,
            "tier_usage": tier_usage,
            "hourly_breakdown": []  # Would be calculated from hourly data
        }
        
        self.data["daily_summary"] = summary
        self.save_data()
        
        return summary
    
    def get_top_users(self, limit: int = 10) -> List[Dict]:
        """Get top users by scan count"""
        user_stats = {}
        
        for log in self.data["scan_logs"]:
            if log["outcome"] == "success":
                email = log["user_email"]
                if email not in user_stats:
                    user_stats[email] = {
                        "email": email,
                        "tier": log["user_tier"],
                        "scan_count": 0
                    }
                user_stats[email]["scan_count"] += 1
                user_stats[email]["tier"] = log["user_tier"]  # Keep latest tier
        
        # Sort by scan count and add usage percentage
        top_users = []
        for user in sorted(user_stats.values(), key=lambda x: x["scan_count"], reverse=True)[:limit]:
            tier_limit = self.tiers[user["tier"]].scan_limit
            usage_percentage = 0 if tier_limit == -1 else (user["scan_count"] / tier_limit) * 100
            
            user["usage_percentage"] = round(usage_percentage, 1)
            user["limit_status"] = "Unlimited" if tier_limit == -1 else f"{usage_percentage:.0f}% of limit"
            top_users.append(user)
        
        return top_users

def demo_usage():
    """Demo the scan tracking system"""
    tracker = ScanUsageTracker()
    
    # Log some demo scans
    scan_id = tracker.log_scan(
        user_email="demo@example.com",
        user_tier="starter",
        agent_name="DealFinderAI",
        scan_type="product_search",
        outcome="success",
        products_found=24,
        processing_time_ms=1247,
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0 (Demo)",
        scan_parameters={"search_query": "demo product", "price_range": "10-50"}
    )
    
    print(f"Logged scan: {scan_id}")
    
    # Check if user can scan
    can_scan, message = tracker.can_user_scan("demo@example.com")
    print(f"Can scan: {can_scan}, Message: {message}")
    
    # Get usage count
    usage = tracker.get_user_scan_count("demo@example.com")
    print(f"Demo user scan count: {usage}")
    
    # Check alerts
    alert = tracker.check_usage_alerts("demo@example.com")
    if alert:
        print(f"Usage alert: {alert['alert_message']}")
    
    # Get upgrade recommendation
    recommendation = tracker.get_upgrade_recommendation("starter")
    if recommendation:
        print(f"Upgrade recommendation: {recommendation}")
    
    # Generate daily summary
    summary = tracker.generate_daily_summary()
    print(f"Daily summary: {summary['total_scans']} total scans")
    
    # Get top users
    top_users = tracker.get_top_users(5)
    print(f"Top users: {len(top_users)} users found")

if __name__ == "__main__":
    demo_usage()
