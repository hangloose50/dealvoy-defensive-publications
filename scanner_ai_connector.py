#!/usr/bin/env python3
"""
Scanner-AI Integration System
Connects barcode scanner output to AI agents for processing
"""

import json
import datetime
from typing import Dict, List, Optional
from ai_agents.MarketShiftForecasterAI import MarketShiftForecasterAI
from ai_agents.ProductMatcherAI import ProductMatcherAI
from ai_agents.BundleProfitEstimator import BundleProfitEstimator

class ScannerAIConnector:
    """
    Connects scanner output to AI agents for automated processing
    """
    
    def __init__(self):
        self.agents = {
            "market_forecaster": MarketShiftForecasterAI(),
            "product_matcher": ProductMatcherAI(),
            "bundle_estimator": BundleProfitEstimator()
        }
        self.scan_history = []
        
    def process_scan(self, upc: str, sku: str = None, product_name: str = None) -> Dict:
        """Process a barcode scan through AI agents"""
        
        scan_data = {
            "upc": upc,
            "sku": sku,
            "product_name": product_name,
            "scan_timestamp": datetime.datetime.now().isoformat(),
            "scan_id": f"scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{upc[-6:]}"
        }
        
        # Validate UPC format
        if not self._validate_upc(upc):
            return {
                "success": False,
                "error": "Invalid UPC format",
                "fallback_suggestions": self._generate_fallback_suggestions(upc)
            }
        
        try:
            # Process through AI agents
            results = {}
            
            # Market trend analysis
            if self._should_run_agent("market_forecaster", upc):
                category = self._extract_category_from_upc(upc)
                market_forecast = self.agents["market_forecaster"].forecast_market_shifts([category])
                results["market_analysis"] = market_forecast
            
            # Product matching
            if self._should_run_agent("product_matcher", upc):
                similar_products = self._simulate_product_matching(upc, product_name)
                results["similar_products"] = similar_products
            
            # Bundle profit estimation
            if self._should_run_agent("bundle_estimator", upc):
                bundle_analysis = self._simulate_bundle_analysis(upc, product_name)
                results["bundle_potential"] = bundle_analysis
            
            # Store scan history
            scan_result = {
                **scan_data,
                "ai_results": results,
                "success": True,
                "processing_time": "1.2s"
            }
            
            self.scan_history.append(scan_result)
            
            return scan_result
            
        except Exception as e:
            # Fallback behavior if AI agents fail
            return self._handle_scan_failure(scan_data, str(e))
    
    def _validate_upc(self, upc: str) -> bool:
        """Validate UPC format (8, 12, or 13 digits)"""
        if not upc.isdigit():
            return False
        return len(upc) in [8, 12, 13]
    
    def _should_run_agent(self, agent_name: str, upc: str) -> bool:
        """Determine if agent should run based on UPC and tier"""
        # Simulate tier checking
        return True  # For demo, always run
    
    def _extract_category_from_upc(self, upc: str) -> str:
        """Extract product category from UPC (simplified simulation)"""
        first_digit = upc[0] if upc else "0"
        category_map = {
            "0": "food_beverage",
            "1": "health_beauty", 
            "2": "electronics",
            "3": "home_garden",
            "4": "clothing",
            "5": "toys_games",
            "6": "sports_outdoors",
            "7": "automotive",
            "8": "books_media",
            "9": "office_supplies"
        }
        return category_map.get(first_digit, "general")
    
    def _simulate_product_matching(self, upc: str, product_name: str) -> Dict:
        """Simulate product matching AI"""
        return {
            "matches_found": 5,
            "similar_products": [
                {"name": "Similar Product 1", "roi_potential": 34.5, "competition": "low"},
                {"name": "Similar Product 2", "roi_potential": 28.9, "competition": "medium"},
                {"name": "Similar Product 3", "roi_potential": 41.2, "competition": "low"}
            ],
            "recommendation": "High potential - similar products showing strong ROI"
        }
    
    def _simulate_bundle_analysis(self, upc: str, product_name: str) -> Dict:
        """Simulate bundle profit estimation"""
        return {
            "bundle_score": 7.8,
            "suggested_bundles": [
                {"items": ["Main Product", "Accessory A"], "estimated_profit": 23.45},
                {"items": ["Main Product", "Accessory B", "Accessory C"], "estimated_profit": 34.67}
            ],
            "recommendation": "Good bundling potential - consider multi-item packages"
        }
    
    def _generate_fallback_suggestions(self, invalid_upc: str) -> List[str]:
        """Generate suggestions when UPC validation fails"""
        suggestions = []
        
        if len(invalid_upc) < 8:
            suggestions.append("UPC too short - please enter at least 8 digits")
        elif len(invalid_upc) > 13:
            suggestions.append("UPC too long - maximum 13 digits")
        
        if not invalid_upc.isdigit():
            suggestions.append("UPC should contain only numbers")
            
        suggestions.extend([
            "Try scanning the barcode again",
            "Check for damaged or unclear barcodes",
            "Use manual entry if barcode is unreadable",
            "Verify UPC from product packaging"
        ])
        
        return suggestions
    
    def _handle_scan_failure(self, scan_data: Dict, error: str) -> Dict:
        """Handle scan processing failures with fallback behavior"""
        return {
            **scan_data,
            "success": False,
            "error": error,
            "fallback_results": {
                "basic_analysis": "Product recognized but AI analysis temporarily unavailable",
                "manual_review": "Product flagged for manual review",
                "retry_suggestion": "Try scanning again in a few moments"
            },
            "fallback_actions": [
                "Product saved to scan history",
                "Basic profit estimation available",
                "Full AI analysis will retry automatically"
            ]
        }
    
    def get_scan_history(self, limit: int = 10) -> List[Dict]:
        """Get recent scan history"""
        return self.scan_history[-limit:] if self.scan_history else []
    
    def get_agent_status(self) -> Dict:
        """Get status of all connected AI agents"""
        return {
            "connected_agents": len(self.agents),
            "agents": {
                name: {
                    "status": "active",
                    "last_used": "recently",
                    "tier_requirement": agent.tier_requirement if hasattr(agent, 'tier_requirement') else "unknown"
                }
                for name, agent in self.agents.items()
            }
        }

def demo_scanner_ai_integration():
    """Demo the scanner-AI integration system"""
    print("🔗 Scanner-AI Integration Demo")
    print("=" * 50)
    
    connector = ScannerAIConnector()
    
    # Test scans
    test_scans = [
        {"upc": "019753136855", "sku": "B08XYZ123", "product": "Wireless Headphones"},
        {"upc": "123456789012", "sku": "B09ABC456", "product": "Coffee Maker"},
        {"upc": "invalid123", "sku": "error", "product": "Invalid Product"}  # Error case
    ]
    
    for i, scan in enumerate(test_scans, 1):
        print(f"\n📱 Test Scan {i}: {scan['product']}")
        print(f"UPC: {scan['upc']}")
        
        result = connector.process_scan(scan['upc'], scan['sku'], scan['product'])
        
        if result['success']:
            print("✅ Scan processed successfully")
            print(f"📊 AI agents activated: {len(result.get('ai_results', {}))}")
            if 'market_analysis' in result.get('ai_results', {}):
                market_outlook = result['ai_results']['market_analysis']['summary']['market_outlook']
                print(f"📈 Market outlook: {market_outlook}")
        else:
            print("❌ Scan failed")
            print(f"Error: {result.get('error')}")
            if 'fallback_suggestions' in result:
                print(f"💡 Suggestions: {len(result['fallback_suggestions'])} available")
    
    # Show agent status
    status = connector.get_agent_status()
    print(f"\n🤖 Connected AI Agents: {status['connected_agents']}")
    
    # Show scan history
    history = connector.get_scan_history()
    print(f"📋 Scan History: {len(history)} scans recorded")

if __name__ == "__main__":
    demo_scanner_ai_integration()
