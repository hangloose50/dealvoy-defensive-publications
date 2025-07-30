#!/usr/bin/env python3
"""
UPCBlacklistDetector - Advanced UPC/barcode validation and blacklist detection
Tier: Starter+ (All Tiers)
Role: Customer AI Agent
"""

import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import re

@dataclass
class UPCValidation:
    upc: str
    is_valid: bool
    is_blacklisted: bool
    blacklist_reason: str
    confidence: float
    category_risk: str

class UPCBlacklistDetector:
    """
    Advanced AI agent for UPC validation and blacklist detection
    - Validates UPC format and check digits
    - Detects known problematic or restricted UPCs
    - Prevents selling restricted or flagged products
    """
    
    def __init__(self):
        self.agent_name = "UPCBlacklistDetector"
        self.tier_requirement = "starter"
        self.category = "compliance_security"
        self.status = "active"
        self.description = "Validates UPCs and detects blacklisted or restricted products"
        
        # Load blacklist database (in real implementation, this would be from external source)
        self.blacklist_db = self._load_blacklist_database()
        
    def validate_upc_batch(self, upcs: List[str]) -> Dict:
        """Validate a batch of UPCs for format, validity, and blacklist status"""
        
        results = []
        
        for upc in upcs:
            validation = self._validate_single_upc(upc)
            results.append(validation)
        
        summary = self._generate_validation_summary(results)
        
        return {
            "validations": [result.__dict__ for result in results],
            "summary": summary,
            "alerts": self._generate_security_alerts(results),
            "recommendations": self._generate_compliance_recommendations(results),
            "validated_at": datetime.datetime.now().isoformat()
        }
    
    def _validate_single_upc(self, upc: str) -> UPCValidation:
        """Validate a single UPC for format, validity, and blacklist status"""
        
        # Clean and normalize UPC
        upc_clean = re.sub(r'[^0-9]', '', upc.strip())
        
        # Check format validity
        is_valid_format = self._check_upc_format(upc_clean)
        
        # Check against blacklist
        blacklist_result = self._check_blacklist(upc_clean)
        
        # Calculate confidence score
        confidence = self._calculate_validation_confidence(upc_clean, is_valid_format, blacklist_result)
        
        return UPCValidation(
            upc=upc_clean,
            is_valid=is_valid_format,
            is_blacklisted=blacklist_result['is_blacklisted'],
            blacklist_reason=blacklist_result['reason'],
            confidence=confidence,
            category_risk=blacklist_result['risk_level']
        )
    
    def _check_upc_format(self, upc: str) -> bool:
        """Check if UPC format is valid"""
        
        # UPC-A should be 12 digits
        if len(upc) != 12:
            return False
        
        # Check if all characters are digits
        if not upc.isdigit():
            return False
        
        # Validate check digit using UPC-A algorithm
        return self._validate_upc_check_digit(upc)
    
    def _validate_upc_check_digit(self, upc: str) -> bool:
        """Validate UPC check digit using standard algorithm"""
        
        if len(upc) != 12:
            return False
        
        # Calculate check digit
        odd_sum = sum(int(upc[i]) for i in range(0, 11, 2))
        even_sum = sum(int(upc[i]) for i in range(1, 11, 2))
        
        total = (odd_sum * 3) + even_sum
        check_digit = (10 - (total % 10)) % 10
        
        return check_digit == int(upc[11])
    
    def _check_blacklist(self, upc: str) -> Dict:
        """Check UPC against blacklist database"""
        
        # Check exact match
        if upc in self.blacklist_db['exact_matches']:
            entry = self.blacklist_db['exact_matches'][upc]
            return {
                'is_blacklisted': True,
                'reason': entry['reason'],
                'risk_level': entry['risk_level']
            }
        
        # Check prefix patterns
        for prefix, info in self.blacklist_db['prefix_patterns'].items():
            if upc.startswith(prefix):
                return {
                    'is_blacklisted': True,
                    'reason': info['reason'],
                    'risk_level': info['risk_level']
                }
        
        # Check category-based restrictions
        category_risk = self._assess_category_risk(upc)
        
        return {
            'is_blacklisted': False,
            'reason': 'No blacklist match found',
            'risk_level': category_risk
        }
    
    def _assess_category_risk(self, upc: str) -> str:
        """Assess risk level based on UPC category patterns"""
        
        # Common UPC prefix categories (simplified)
        category_patterns = {
            '0': 'regular_products',
            '1': 'reserved',
            '2': 'random_weight',
            '3': 'pharmaceuticals',
            '4': 'restricted_items',
            '5': 'coupons',
            '6': 'regular_products',
            '7': 'regular_products', 
            '8': 'regular_products',
            '9': 'reserved'
        }
        
        first_digit = upc[0] if upc else '0'
        category = category_patterns.get(first_digit, 'unknown')
        
        risk_levels = {
            'pharmaceuticals': 'high',
            'restricted_items': 'high',
            'reserved': 'medium',
            'coupons': 'medium',
            'random_weight': 'low',
            'regular_products': 'low',
            'unknown': 'medium'
        }
        
        return risk_levels.get(category, 'medium')
    
    def _calculate_validation_confidence(self, upc: str, is_valid: bool, blacklist_result: Dict) -> float:
        """Calculate confidence score for validation"""
        
        confidence = 0.5  # Base confidence
        
        # Format validity adds confidence
        if is_valid:
            confidence += 0.3
        else:
            confidence -= 0.2
        
        # Blacklist certainty
        if blacklist_result['is_blacklisted']:
            confidence += 0.2  # High confidence in blacklist detection
        else:
            confidence += 0.1  # Moderate confidence in clean status
        
        # Risk level affects confidence
        risk_adjustments = {
            'low': 0.1,
            'medium': 0.0,
            'high': -0.1
        }
        confidence += risk_adjustments.get(blacklist_result['risk_level'], 0.0)
        
        return round(max(0.0, min(1.0, confidence)), 2)
    
    def _load_blacklist_database(self) -> Dict:
        """Load blacklist database (simulated for demo)"""
        
        return {
            'exact_matches': {
                '123456789012': {
                    'reason': 'Counterfeit product detected',
                    'risk_level': 'high',
                    'added_date': '2024-01-15'
                },
                '987654321098': {
                    'reason': 'Recalled product - safety issue',
                    'risk_level': 'high',
                    'added_date': '2024-02-20'
                },
                '555666777888': {
                    'reason': 'Copyright infringement',
                    'risk_level': 'high',
                    'added_date': '2024-03-10'
                }
            },
            'prefix_patterns': {
                '999': {
                    'reason': 'Test/internal use codes',
                    'risk_level': 'medium'
                },
                '666': {
                    'reason': 'Restricted category prefix',
                    'risk_level': 'high'
                },
                '000': {
                    'reason': 'Invalid/placeholder codes',
                    'risk_level': 'medium'
                }
            },
            'category_restrictions': {
                'pharmaceuticals': 'Requires special licensing',
                'firearms': 'Prohibited on most platforms',
                'adult_content': 'Age-restricted sales only'
            }
        }
    
    def _generate_validation_summary(self, results: List[UPCValidation]) -> Dict:
        """Generate summary of validation results"""
        
        total = len(results)
        valid_count = len([r for r in results if r.is_valid])
        blacklisted_count = len([r for r in results if r.is_blacklisted])
        high_risk_count = len([r for r in results if r.category_risk == 'high'])
        
        avg_confidence = sum(r.confidence for r in results) / total if total > 0 else 0.0
        
        return {
            'total_upcs': total,
            'valid_format': valid_count,
            'blacklisted': blacklisted_count,
            'high_risk': high_risk_count,
            'success_rate': round((valid_count - blacklisted_count) / total * 100, 1) if total > 0 else 0.0,
            'average_confidence': round(avg_confidence, 2)
        }
    
    def _generate_security_alerts(self, results: List[UPCValidation]) -> List[Dict]:
        """Generate security alerts based on validation results"""
        
        alerts = []
        
        blacklisted = [r for r in results if r.is_blacklisted]
        if blacklisted:
            alerts.append({
                'type': 'blacklist_detection',
                'severity': 'critical',
                'count': len(blacklisted),
                'message': f'Found {len(blacklisted)} blacklisted UPC(s)',
                'action_required': 'Remove from inventory immediately'
            })
        
        high_risk = [r for r in results if r.category_risk == 'high' and not r.is_blacklisted]
        if high_risk:
            alerts.append({
                'type': 'high_risk_category',
                'severity': 'warning',
                'count': len(high_risk),
                'message': f'Found {len(high_risk)} high-risk category UPC(s)',
                'action_required': 'Review compliance requirements'
            })
        
        invalid_format = [r for r in results if not r.is_valid]
        if invalid_format:
            alerts.append({
                'type': 'format_validation',
                'severity': 'minor',
                'count': len(invalid_format),
                'message': f'Found {len(invalid_format)} invalid UPC format(s)',
                'action_required': 'Verify and correct UPC data'
            })
        
        return alerts
    
    def _generate_compliance_recommendations(self, results: List[UPCValidation]) -> List[Dict]:
        """Generate compliance recommendations"""
        
        recommendations = []
        
        blacklisted_count = len([r for r in results if r.is_blacklisted])
        if blacklisted_count > 0:
            recommendations.append({
                'priority': 'immediate',
                'category': 'compliance',
                'recommendation': 'Implement automated blacklist checking before listing',
                'impact': 'Prevents legal issues and account suspension'
            })
        
        high_risk_count = len([r for r in results if r.category_risk == 'high'])
        if high_risk_count > 5:  # Threshold for recommendation
            recommendations.append({
                'priority': 'high',
                'category': 'risk_management',
                'recommendation': 'Review high-risk product categories and compliance requirements',
                'impact': 'Reduces regulatory risks and potential penalties'
            })
        
        invalid_count = len([r for r in results if not r.is_valid])
        if invalid_count > 0:
            recommendations.append({
                'priority': 'medium',
                'category': 'data_quality',
                'recommendation': 'Implement UPC validation in product data entry process',
                'impact': 'Improves data quality and reduces listing errors'
            })
        
        return recommendations
    
    def get_agent_info(self) -> Dict:
        """Return agent information for dashboard display"""
        return {
            "name": self.agent_name,
            "tier_requirement": self.tier_requirement,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "icon": "🛡️",
            "features": [
                "UPC format validation",
                "Blacklist detection",
                "Risk assessment",
                "Compliance checking",
                "Batch processing"
            ],
            "tier_badge": "All Tiers",
            "tooltip": "Prevent selling restricted products with UPC validation and blacklist detection"
        }

def demo_upc_detector():
    """Demo the UPCBlacklistDetector"""
    agent = UPCBlacklistDetector()
    
    # Test UPCs (mix of valid, invalid, and blacklisted)
    test_upcs = [
        "123456789012",  # Blacklisted
        "036000291452",  # Valid Coca-Cola UPC
        "987654321098",  # Blacklisted (recalled)
        "invalid-upc",   # Invalid format
        "999123456789",  # Test prefix (medium risk)
        "666123456789"   # Restricted prefix (high risk)
    ]
    
    # Validate UPCs
    results = agent.validate_upc_batch(test_upcs)
    
    print("🛡️ UPC Blacklist Detection Results:")
    print("=" * 50)
    print(f"Total UPCs: {results['summary']['total_upcs']}")
    print(f"Valid Format: {results['summary']['valid_format']}")
    print(f"Blacklisted: {results['summary']['blacklisted']}")
    print(f"High Risk: {results['summary']['high_risk']}")
    print(f"Success Rate: {results['summary']['success_rate']}%")
    
    print(f"\n🚨 Security Alerts:")
    for alert in results['alerts']:
        severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡" if alert['severity'] == 'warning' else "🔵"
        print(f"{severity_icon} {alert['message']}")
    
    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        priority_icon = "🚨" if rec['priority'] == 'immediate' else "🔴" if rec['priority'] == 'high' else "🟡"
        print(f"{priority_icon} {rec['recommendation']}")
    
    return results

if __name__ == "__main__":
    demo_upc_detector()
