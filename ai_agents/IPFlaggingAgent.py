#!/usr/bin/env python3
"""
IPFlaggingAgent - Advanced IP address analysis and security flagging
Tier: Enterprise+ (Tier 3+) - Admin Only
Role: Admin-Only AI Agent
"""

import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import ipaddress
import re

@dataclass
class IPAnalysis:
    ip_address: str
    is_valid: bool
    ip_type: str  # 'public', 'private', 'reserved', 'multicast'
    geolocation: Dict
    threat_level: str  # 'low', 'medium', 'high', 'critical'
    reputation_score: float
    flags: List[str]
    recommendations: List[str]

class IPFlaggingAgent:
    """
    Advanced AI agent for IP address analysis and security flagging (ADMIN ONLY)
    - Analyzes IP addresses for security threats and anomalies
    - Provides geolocation and reputation analysis
    - Flags suspicious IPs for admin review
    - Enterprise+ tier with admin-only access
    """
    
    def __init__(self):
        self.agent_name = "IPFlaggingAgent"
        self.tier_requirement = "enterprise"
        self.category = "security_admin"
        self.status = "active"
        self.description = "Advanced IP analysis and threat detection (Admin Only)"
        self.admin_only = True  # Critical: Admin-only agent
        
        # Load threat intelligence database
        self.threat_db = self._load_threat_database()
        
    def analyze_ip_batch(self, ip_addresses: List[str], context: str = "general") -> Dict:
        """Analyze a batch of IP addresses for security threats"""
        
        analyses = []
        
        for ip in ip_addresses:
            analysis = self._analyze_single_ip(ip, context)
            analyses.append(analysis)
        
        summary = self._generate_security_summary(analyses)
        
        return {
            "ip_analyses": [analysis.__dict__ for analysis in analyses],
            "security_summary": summary,
            "threat_alerts": self._generate_threat_alerts(analyses),
            "admin_recommendations": self._generate_admin_recommendations(analyses),
            "analysis_context": context,
            "analyzed_at": datetime.datetime.now().isoformat()
        }
    
    def _analyze_single_ip(self, ip: str, context: str) -> IPAnalysis:
        """Analyze a single IP address for security threats"""
        
        # Validate IP format
        is_valid, ip_obj = self._validate_ip_format(ip)
        
        if not is_valid:
            return IPAnalysis(
                ip_address=ip,
                is_valid=False,
                ip_type="invalid",
                geolocation={},
                threat_level="unknown",
                reputation_score=0.0,
                flags=["Invalid IP format"],
                recommendations=["Verify IP address format"]
            )
        
        # Determine IP type
        ip_type = self._classify_ip_type(ip_obj)
        
        # Get geolocation (simulated)
        geolocation = self._get_geolocation(ip)
        
        # Check threat databases
        threat_analysis = self._check_threat_databases(ip)
        
        # Calculate reputation score
        reputation_score = self._calculate_reputation_score(ip, threat_analysis, geolocation)
        
        # Determine threat level
        threat_level = self._determine_threat_level(reputation_score, threat_analysis)
        
        # Generate flags and recommendations
        flags = self._generate_ip_flags(ip, threat_analysis, geolocation, context)
        recommendations = self._generate_ip_recommendations(threat_level, flags)
        
        return IPAnalysis(
            ip_address=ip,
            is_valid=True,
            ip_type=ip_type,
            geolocation=geolocation,
            threat_level=threat_level,
            reputation_score=reputation_score,
            flags=flags,
            recommendations=recommendations
        )
    
    def _validate_ip_format(self, ip: str) -> tuple:
        """Validate IP address format"""
        try:
            ip_obj = ipaddress.ip_address(ip.strip())
            return True, ip_obj
        except ValueError:
            return False, None
    
    def _classify_ip_type(self, ip_obj) -> str:
        """Classify IP address type"""
        if ip_obj.is_private:
            return "private"
        elif ip_obj.is_reserved:
            return "reserved"
        elif ip_obj.is_multicast:
            return "multicast"
        elif ip_obj.is_loopback:
            return "loopback"
        else:
            return "public"
    
    def _get_geolocation(self, ip: str) -> Dict:
        """Get geolocation data for IP (simulated)"""
        
        # Simulated geolocation data
        geo_database = {
            "192.168.1.1": {"country": "Private", "city": "Local", "isp": "Private Network"},
            "8.8.8.8": {"country": "US", "city": "Mountain View", "isp": "Google LLC"},
            "1.1.1.1": {"country": "US", "city": "San Francisco", "isp": "Cloudflare"},
            "203.0.113.1": {"country": "Unknown", "city": "Test Network", "isp": "RFC 5737"}
        }
        
        return geo_database.get(ip, {
            "country": "Unknown",
            "city": "Unknown", 
            "isp": "Unknown",
            "coordinates": {"lat": 0.0, "lon": 0.0}
        })
    
    def _check_threat_databases(self, ip: str) -> Dict:
        """Check IP against threat intelligence databases"""
        
        threats = {
            "malware": False,
            "botnet": False,
            "tor_exit": False,
            "vpn_proxy": False,
            "known_attacker": False,
            "reputation_lists": []
        }
        
        # Check against known threat IPs
        if ip in self.threat_db["malware_ips"]:
            threats["malware"] = True
            threats["reputation_lists"].append("Malware Command & Control")
        
        if ip in self.threat_db["botnet_ips"]:
            threats["botnet"] = True
            threats["reputation_lists"].append("Botnet Member")
        
        if ip in self.threat_db["tor_exits"]:
            threats["tor_exit"] = True
            threats["reputation_lists"].append("Tor Exit Node")
        
        if ip in self.threat_db["vpn_proxies"]:
            threats["vpn_proxy"] = True
            threats["reputation_lists"].append("VPN/Proxy Service")
        
        if ip in self.threat_db["known_attackers"]:
            threats["known_attacker"] = True
            threats["reputation_lists"].append("Known Attacker")
        
        return threats
    
    def _calculate_reputation_score(self, ip: str, threats: Dict, geo: Dict) -> float:
        """Calculate IP reputation score (0.0 = bad, 1.0 = good)"""
        
        score = 1.0  # Start with perfect score
        
        # Threat penalties
        if threats["malware"]:
            score -= 0.8
        if threats["botnet"]:
            score -= 0.7
        if threats["known_attacker"]:
            score -= 0.9
        if threats["tor_exit"]:
            score -= 0.3
        if threats["vpn_proxy"]:
            score -= 0.2
        
        # Geographic risk factors
        high_risk_countries = ["CN", "RU", "KP", "IR"]
        if geo.get("country") in high_risk_countries:
            score -= 0.1
        
        # ISP risk factors
        suspicious_isps = ["Unknown", "Hosting Provider", "VPS Service"]
        if any(susp in geo.get("isp", "") for susp in suspicious_isps):
            score -= 0.1
        
        return round(max(0.0, min(1.0, score)), 2)
    
    def _determine_threat_level(self, reputation: float, threats: Dict) -> str:
        """Determine overall threat level"""
        
        if threats["malware"] or threats["known_attacker"] or reputation < 0.2:
            return "critical"
        elif threats["botnet"] or reputation < 0.4:
            return "high"
        elif threats["tor_exit"] or threats["vpn_proxy"] or reputation < 0.7:
            return "medium"
        else:
            return "low"
    
    def _generate_ip_flags(self, ip: str, threats: Dict, geo: Dict, context: str) -> List[str]:
        """Generate security flags for IP"""
        
        flags = []
        
        if threats["malware"]:
            flags.append("MALWARE_C2")
        if threats["botnet"]:
            flags.append("BOTNET_MEMBER")
        if threats["known_attacker"]:
            flags.append("KNOWN_ATTACKER")
        if threats["tor_exit"]:
            flags.append("TOR_EXIT_NODE")
        if threats["vpn_proxy"]:
            flags.append("VPN_PROXY")
        
        # Context-specific flags
        if context == "login_attempt" and (threats["tor_exit"] or threats["vpn_proxy"]):
            flags.append("SUSPICIOUS_LOGIN_SOURCE")
        
        if context == "api_access" and threats["botnet"]:
            flags.append("AUTOMATED_ACCESS_RISK")
        
        # Geographic flags
        if geo.get("country") in ["CN", "RU", "KP", "IR"]:
            flags.append("HIGH_RISK_GEOGRAPHY")
        
        return flags
    
    def _generate_ip_recommendations(self, threat_level: str, flags: List[str]) -> List[str]:
        """Generate admin recommendations for IP handling"""
        
        recommendations = []
        
        if threat_level == "critical":
            recommendations.append("IMMEDIATE BLOCK - Critical threat detected")
            recommendations.append("Review all recent activity from this IP")
            recommendations.append("Check for compromise indicators")
        
        elif threat_level == "high":
            recommendations.append("Consider blocking or rate limiting")
            recommendations.append("Increase monitoring for this IP")
            recommendations.append("Require additional authentication")
        
        elif threat_level == "medium":
            recommendations.append("Monitor closely for suspicious activity")
            recommendations.append("Consider implementing CAPTCHAs")
            recommendations.append("Log all interactions for review")
        
        # Flag-specific recommendations
        if "TOR_EXIT_NODE" in flags:
            recommendations.append("Consider Tor policy enforcement")
        
        if "VPN_PROXY" in flags:
            recommendations.append("Evaluate VPN/proxy access policies")
        
        if "HIGH_RISK_GEOGRAPHY" in flags:
            recommendations.append("Apply geo-specific security measures")
        
        return recommendations
    
    def _load_threat_database(self) -> Dict:
        """Load threat intelligence database (simulated)"""
        
        return {
            "malware_ips": [
                "198.51.100.1",
                "203.0.113.5",
                "192.0.2.10"
            ],
            "botnet_ips": [
                "198.51.100.2",
                "203.0.113.6"
            ],
            "tor_exits": [
                "198.51.100.3",
                "203.0.113.7"
            ],
            "vpn_proxies": [
                "198.51.100.4",
                "203.0.113.8"
            ],
            "known_attackers": [
                "198.51.100.5",
                "203.0.113.9"
            ]
        }
    
    def _generate_security_summary(self, analyses: List[IPAnalysis]) -> Dict:
        """Generate security summary for admin dashboard"""
        
        total = len(analyses)
        critical = len([a for a in analyses if a.threat_level == "critical"])
        high = len([a for a in analyses if a.threat_level == "high"])
        medium = len([a for a in analyses if a.threat_level == "medium"])
        low = len([a for a in analyses if a.threat_level == "low"])
        
        avg_reputation = sum(a.reputation_score for a in analyses) / total if total > 0 else 0.0
        
        return {
            "total_ips": total,
            "threat_distribution": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },
            "average_reputation": round(avg_reputation, 2),
            "immediate_action_required": critical + high,
            "monitoring_recommended": medium
        }
    
    def _generate_threat_alerts(self, analyses: List[IPAnalysis]) -> List[Dict]:
        """Generate threat alerts for admin attention"""
        
        alerts = []
        
        critical_ips = [a for a in analyses if a.threat_level == "critical"]
        if critical_ips:
            alerts.append({
                "severity": "critical",
                "type": "immediate_threat",
                "count": len(critical_ips),
                "message": f"CRITICAL: {len(critical_ips)} IP(s) pose immediate security threat",
                "action": "Block immediately and investigate"
            })
        
        malware_ips = [a for a in analyses if "MALWARE_C2" in a.flags]
        if malware_ips:
            alerts.append({
                "severity": "critical", 
                "type": "malware_detection",
                "count": len(malware_ips),
                "message": f"Malware C&C detected from {len(malware_ips)} IP(s)",
                "action": "Immediate security response required"
            })
        
        tor_ips = [a for a in analyses if "TOR_EXIT_NODE" in a.flags]
        if len(tor_ips) > 3:  # Threshold for alert
            alerts.append({
                "severity": "medium",
                "type": "anonymization_network",
                "count": len(tor_ips),
                "message": f"High volume of Tor traffic detected ({len(tor_ips)} IPs)",
                "action": "Review Tor access policies"
            })
        
        return alerts
    
    def _generate_admin_recommendations(self, analyses: List[IPAnalysis]) -> List[Dict]:
        """Generate strategic recommendations for admin"""
        
        recommendations = []
        
        threat_count = len([a for a in analyses if a.threat_level in ["critical", "high"]])
        if threat_count > len(analyses) * 0.1:  # More than 10% are threats
            recommendations.append({
                "priority": "high",
                "category": "security_posture",
                "recommendation": "Implement automated IP threat blocking",
                "rationale": f"High threat ratio detected: {threat_count}/{len(analyses)} IPs"
            })
        
        geo_diversity = len(set(a.geolocation.get("country", "Unknown") for a in analyses))
        if geo_diversity > 20:  # High geographic diversity
            recommendations.append({
                "priority": "medium",
                "category": "geographic_controls",
                "recommendation": "Consider implementing geo-blocking for high-risk regions",
                "rationale": f"Traffic from {geo_diversity} different countries detected"
            })
        
        vpn_count = len([a for a in analyses if "VPN_PROXY" in a.flags])
        if vpn_count > 5:
            recommendations.append({
                "priority": "medium", 
                "category": "access_control",
                "recommendation": "Evaluate VPN/proxy access policies",
                "rationale": f"Significant VPN/proxy usage detected: {vpn_count} IPs"
            })
        
        return recommendations
    
    def get_agent_info(self) -> Dict:
        """Return agent information for admin dashboard display"""
        return {
            "name": self.agent_name,
            "tier_requirement": self.tier_requirement,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "admin_only": self.admin_only,
            "icon": "🔒",
            "features": [
                "IP threat analysis",
                "Geolocation intelligence",
                "Reputation scoring",
                "Security flagging",
                "Admin threat alerts"
            ],
            "tier_badge": "Enterprise+ (Admin)",
            "tooltip": "Advanced IP security analysis for threat detection and admin oversight"
        }

def demo_ip_flagging():
    """Demo the IPFlaggingAgent (Admin only)"""
    agent = IPFlaggingAgent()
    
    # Test IPs (mix of clean, suspicious, and malicious)
    test_ips = [
        "8.8.8.8",           # Google DNS (clean)
        "198.51.100.1",      # Malware C&C (critical)
        "203.0.113.6",       # Botnet member (high)
        "192.168.1.1",      # Private IP (low)
        "198.51.100.3",      # Tor exit (medium)
        "invalid-ip"         # Invalid format
    ]
    
    # Analyze IPs
    results = agent.analyze_ip_batch(test_ips, "login_attempt")
    
    print("🔒 IP Security Analysis Results (ADMIN ONLY):")
    print("=" * 60)
    print(f"Total IPs Analyzed: {results['security_summary']['total_ips']}")
    print(f"Critical Threats: {results['security_summary']['threat_distribution']['critical']}")
    print(f"High Threats: {results['security_summary']['threat_distribution']['high']}")
    print(f"Immediate Action Required: {results['security_summary']['immediate_action_required']}")
    print(f"Average Reputation: {results['security_summary']['average_reputation']:.2f}")
    
    print(f"\n🚨 Threat Alerts:")
    for alert in results['threat_alerts']:
        severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡" if alert['severity'] == 'medium' else "🟢"
        print(f"{severity_icon} {alert['message']}")
    
    print(f"\n📊 IP Analysis Details:")
    for ip_data in results['ip_analyses'][:3]:  # Show first 3
        threat_icon = "🔴" if ip_data['threat_level'] == 'critical' else "🟡" if ip_data['threat_level'] == 'high' else "🟢"
        print(f"{threat_icon} {ip_data['ip_address']}: {ip_data['threat_level'].upper()} (Score: {ip_data['reputation_score']})")
        if ip_data['flags']:
            print(f"   Flags: {', '.join(ip_data['flags'])}")
    
    return results

if __name__ == "__main__":
    print("⚠️  ADMIN-ONLY AGENT - Requires Enterprise+ privileges")
    demo_ip_flagging()
