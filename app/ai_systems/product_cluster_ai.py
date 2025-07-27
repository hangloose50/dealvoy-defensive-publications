#!/usr/bin/env python3
"""
🔗 ProductCluster AI - Groups related products and identifies bundling opportunities
Smart product relationship analysis for e-commerce optimization
"""

import json
import time
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict

class ProductClusterAI:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.reports_dir = self.project_path / "dist" / "intelligence_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.clustering_algorithms = self._initialize_clustering_algorithms()
        
    def _initialize_clustering_algorithms(self) -> Dict[str, Any]:
        """Initialize clustering algorithms and similarity metrics"""
        return {
            "similarity_weights": {
                "category": 0.25,
                "brand": 0.20,
                "price_range": 0.15,
                "keywords": 0.20,
                "customer_demographics": 0.10,
                "seasonal_patterns": 0.10
            },
            "cluster_types": {
                "complementary": "Products often bought together",
                "substitute": "Alternative products for same need",
                "upgrade": "Premium versions of base products",
                "accessory": "Add-on products for main items",
                "bundle": "Products that create value when combined"
            },
            "bundling_rules": {
                "max_price_variance": 0.7,  # Products shouldn't vary by more than 70% in price
                "min_similarity_score": 0.6,  # Minimum similarity to consider bundling
                "optimal_bundle_size": (2, 4),  # 2-4 products per bundle typically optimal
                "margin_improvement_target": 0.15  # Target 15% margin improvement through bundling
            }
        }
    
    def calculate_product_similarity(self, product1: Dict[str, Any], product2: Dict[str, Any]) -> float:
        """Calculate similarity score between two products"""
        similarity_score = 0.0
        weights = self.clustering_algorithms["similarity_weights"]
        
        # Category similarity
        cat1 = product1.get("category", "").lower()
        cat2 = product2.get("category", "").lower()
        if cat1 == cat2:
            similarity_score += weights["category"] * 1.0
        elif any(word in cat2 for word in cat1.split()) or any(word in cat1 for word in cat2.split()):
            similarity_score += weights["category"] * 0.7
        
        # Brand similarity
        brand1 = product1.get("brand", "").lower()
        brand2 = product2.get("brand", "").lower()
        if brand1 == brand2:
            similarity_score += weights["brand"] * 1.0
        elif brand1 and brand2 and (brand1 in brand2 or brand2 in brand1):
            similarity_score += weights["brand"] * 0.5
        
        # Price range similarity
        price1 = product1.get("price", 0)
        price2 = product2.get("price", 0)
        if price1 > 0 and price2 > 0:
            price_ratio = min(price1, price2) / max(price1, price2)
            if price_ratio > 0.8:
                similarity_score += weights["price_range"] * 1.0
            elif price_ratio > 0.5:
                similarity_score += weights["price_range"] * 0.7
            elif price_ratio > 0.3:
                similarity_score += weights["price_range"] * 0.4
        
        # Keyword similarity
        keywords1 = set(product1.get("keywords", []))
        keywords2 = set(product2.get("keywords", []))
        if keywords1 and keywords2:
            intersection = len(keywords1.intersection(keywords2))
            union = len(keywords1.union(keywords2))
            keyword_similarity = intersection / union if union > 0 else 0
            similarity_score += weights["keywords"] * keyword_similarity
        
        # Customer demographics similarity
        demo1 = product1.get("target_demographic", "")
        demo2 = product2.get("target_demographic", "")
        if demo1 == demo2:
            similarity_score += weights["customer_demographics"] * 1.0
        elif demo1 and demo2:
            similarity_score += weights["customer_demographics"] * 0.5
        
        # Seasonal patterns similarity
        season1 = product1.get("seasonal_pattern", "")
        season2 = product2.get("seasonal_pattern", "")
        if season1 == season2:
            similarity_score += weights["seasonal_patterns"] * 1.0
        
        return min(similarity_score, 1.0)
    
    def identify_product_clusters(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify clusters of related products"""
        clusters = []
        processed_products = set()
        
        for i, product in enumerate(products):
            if i in processed_products:
                continue
            
            cluster = {
                "cluster_id": f"cluster_{len(clusters) + 1}",
                "products": [product],
                "product_indices": [i],
                "center_product": product,
                "cluster_type": "single",
                "similarity_scores": []
            }
            
            # Find similar products
            for j, other_product in enumerate(products):
                if i != j and j not in processed_products:
                    similarity = self.calculate_product_similarity(product, other_product)
                    
                    if similarity >= self.clustering_algorithms["bundling_rules"]["min_similarity_score"]:
                        cluster["products"].append(other_product)
                        cluster["product_indices"].append(j)
                        cluster["similarity_scores"].append(similarity)
                        processed_products.add(j)
            
            # Determine cluster type
            if len(cluster["products"]) > 1:
                cluster["cluster_type"] = self._determine_cluster_type(cluster["products"])
                cluster["avg_similarity"] = sum(cluster["similarity_scores"]) / len(cluster["similarity_scores"])
            
            processed_products.add(i)
            clusters.append(cluster)
        
        return {
            "clusters": clusters,
            "total_products": len(products),
            "total_clusters": len(clusters),
            "clustered_products": sum(len(c["products"]) for c in clusters if len(c["products"]) > 1),
            "clustering_efficiency": len([c for c in clusters if len(c["products"]) > 1]) / len(clusters) if clusters else 0
        }
    
    def _determine_cluster_type(self, products: List[Dict[str, Any]]) -> str:
        """Determine the type of relationship between clustered products"""
        categories = [p.get("category", "") for p in products]
        brands = [p.get("brand", "") for p in products]
        prices = [p.get("price", 0) for p in products if p.get("price", 0) > 0]
        
        # Same category, different brands = substitute
        if len(set(categories)) == 1 and len(set(brands)) > 1:
            return "substitute"
        
        # Same brand, different categories = complementary
        if len(set(brands)) == 1 and len(set(categories)) > 1:
            return "complementary"
        
        # Significant price differences = upgrade/downgrade
        if prices and max(prices) / min(prices) > 2:
            return "upgrade"
        
        # Different categories, similar use cases = bundle
        if len(set(categories)) > 1:
            return "bundle"
        
        return "complementary"
    
    def analyze_bundling_opportunities(self, clusters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze which clusters present good bundling opportunities"""
        bundling_opportunities = []
        
        for cluster in clusters["clusters"]:
            if len(cluster["products"]) < 2:
                continue
            
            bundle_analysis = self._analyze_bundle_potential(cluster)
            if bundle_analysis["bundle_score"] > 0.6:
                bundling_opportunities.append(bundle_analysis)
        
        # Sort by bundle score
        bundling_opportunities.sort(key=lambda x: x["bundle_score"], reverse=True)
        
        return {
            "opportunities": bundling_opportunities,
            "total_opportunities": len(bundling_opportunities),
            "high_potential": len([o for o in bundling_opportunities if o["bundle_score"] > 0.8]),
            "medium_potential": len([o for o in bundling_opportunities if 0.6 <= o["bundle_score"] <= 0.8])
        }
    
    def _analyze_bundle_potential(self, cluster: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze bundling potential for a cluster"""
        products = cluster["products"]
        
        # Calculate bundle metrics
        total_individual_price = sum(p.get("price", 0) for p in products)
        avg_margin = sum(p.get("margin", 0.2) for p in products) / len(products)
        
        # Proposed bundle price (10-15% discount)
        bundle_discount = 0.125  # 12.5% average discount
        bundle_price = total_individual_price * (1 - bundle_discount)
        
        # Calculate bundle score
        score_factors = {
            "price_attractiveness": self._calculate_price_attractiveness(total_individual_price, bundle_price),
            "product_complementarity": cluster.get("avg_similarity", 0.5),
            "margin_preservation": min(avg_margin / 0.2, 1.0),  # Normalized to 20% target
            "bundle_size_optimization": self._calculate_size_score(len(products)),
            "category_diversity": self._calculate_diversity_score(products)
        }
        
        bundle_score = sum(score_factors.values()) / len(score_factors)
        
        return {
            "cluster_id": cluster["cluster_id"],
            "products": products,
            "bundle_score": round(bundle_score, 3),
            "score_factors": score_factors,
            "pricing": {
                "individual_total": total_individual_price,
                "bundle_price": round(bundle_price, 2),
                "customer_savings": round(total_individual_price - bundle_price, 2),
                "discount_percentage": round(bundle_discount * 100, 1)
            },
            "recommendation": self._get_bundle_recommendation(bundle_score),
            "bundle_type": cluster.get("cluster_type", "complementary")
        }
    
    def _calculate_price_attractiveness(self, individual_total: float, bundle_price: float) -> float:
        """Calculate how attractive the bundle pricing is"""
        savings_percentage = (individual_total - bundle_price) / individual_total
        
        # Optimal savings range is 10-20%
        if 0.10 <= savings_percentage <= 0.20:
            return 1.0
        elif 0.05 <= savings_percentage <= 0.25:
            return 0.8
        elif savings_percentage > 0:
            return 0.6
        else:
            return 0.0
    
    def _calculate_size_score(self, bundle_size: int) -> float:
        """Calculate optimal bundle size score"""
        optimal_min, optimal_max = self.clustering_algorithms["bundling_rules"]["optimal_bundle_size"]
        
        if optimal_min <= bundle_size <= optimal_max:
            return 1.0
        elif bundle_size == optimal_max + 1 or bundle_size == optimal_min - 1:
            return 0.8
        else:
            return 0.5
    
    def _calculate_diversity_score(self, products: List[Dict[str, Any]]) -> float:
        """Calculate category diversity score"""
        categories = set(p.get("category", "") for p in products)
        
        # Some diversity is good, but not too much
        if len(categories) == 2:
            return 1.0
        elif len(categories) == 3:
            return 0.8
        elif len(categories) == 1:
            return 0.6
        else:
            return 0.4
    
    def _get_bundle_recommendation(self, score: float) -> str:
        """Get recommendation based on bundle score"""
        if score >= 0.8:
            return "EXCELLENT: High-potential bundle opportunity"
        elif score >= 0.6:
            return "GOOD: Viable bundling opportunity"
        elif score >= 0.4:
            return "FAIR: Consider with modifications"
        else:
            return "POOR: Not recommended for bundling"
    
    def generate_cross_sell_recommendations(self, product: Dict[str, Any], all_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate cross-sell recommendations for a specific product"""
        recommendations = []
        
        for other_product in all_products:
            if other_product.get("name") == product.get("name"):
                continue
            
            similarity = self.calculate_product_similarity(product, other_product)
            
            if similarity > 0.4:  # Lower threshold for cross-sell
                cross_sell_score = self._calculate_cross_sell_score(product, other_product, similarity)
                
                recommendations.append({
                    "product": other_product,
                    "similarity_score": round(similarity, 3),
                    "cross_sell_score": round(cross_sell_score, 3),
                    "relationship_type": self._determine_relationship_type(product, other_product),
                    "recommendation_strength": self._get_cross_sell_strength(cross_sell_score)
                })
        
        # Sort by cross-sell score
        recommendations.sort(key=lambda x: x["cross_sell_score"], reverse=True)
        return recommendations[:10]  # Top 10 recommendations
    
    def _calculate_cross_sell_score(self, main_product: Dict[str, Any], 
                                  cross_product: Dict[str, Any], similarity: float) -> float:
        """Calculate cross-sell potential score"""
        base_score = similarity * 0.6
        
        # Price compatibility (not too expensive relative to main product)
        main_price = main_product.get("price", 0)
        cross_price = cross_product.get("price", 0)
        
        if main_price > 0 and cross_price > 0:
            price_ratio = cross_price / main_price
            if 0.3 <= price_ratio <= 1.5:  # Cross-sell item should be 30%-150% of main price
                base_score += 0.3
            elif 0.1 <= price_ratio <= 2.0:
                base_score += 0.2
        
        # Margin consideration
        cross_margin = cross_product.get("margin", 0.2)
        if cross_margin > 0.25:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _determine_relationship_type(self, product1: Dict[str, Any], product2: Dict[str, Any]) -> str:
        """Determine relationship type between two products"""
        cat1 = product1.get("category", "").lower()
        cat2 = product2.get("category", "").lower()
        price1 = product1.get("price", 0)
        price2 = product2.get("price", 0)
        
        if cat1 == cat2:
            if abs(price1 - price2) / max(price1, price2, 1) < 0.2:
                return "alternative"
            else:
                return "upgrade" if price2 > price1 else "budget_option"
        else:
            return "complementary"
    
    def _get_cross_sell_strength(self, score: float) -> str:
        """Convert cross-sell score to strength rating"""
        if score >= 0.8:
            return "STRONG"
        elif score >= 0.6:
            return "MEDIUM"
        elif score >= 0.4:
            return "WEAK"
        else:
            return "MINIMAL"
    
    def run(self) -> Dict[str, Any]:
        """Main execution function"""
        print("🔗 [ProductCluster AI] Analyzing product relationships...")
        
        # Sample product data for clustering analysis
        sample_products = [
            {
                "name": "Wireless Bluetooth Earbuds",
                "category": "Electronics/Audio",
                "brand": "Sony",
                "price": 49.99,
                "margin": 0.25,
                "keywords": ["wireless", "bluetooth", "audio", "music"],
                "target_demographic": "tech-savvy",
                "seasonal_pattern": "consistent"
            },
            {
                "name": "Phone Charging Cable",
                "category": "Electronics/Accessories",
                "brand": "Anker",
                "price": 12.99,
                "margin": 0.35,
                "keywords": ["charging", "cable", "phone", "usb"],
                "target_demographic": "tech-savvy",
                "seasonal_pattern": "consistent"
            },
            {
                "name": "Portable Phone Stand",
                "category": "Electronics/Accessories",
                "brand": "Generic",
                "price": 8.99,
                "margin": 0.40,
                "keywords": ["phone", "stand", "desk", "portable"],
                "target_demographic": "professionals",
                "seasonal_pattern": "consistent"
            },
            {
                "name": "Kitchen Storage Containers",
                "category": "Home/Kitchen",
                "brand": "Rubbermaid",
                "price": 24.99,
                "margin": 0.30,
                "keywords": ["storage", "kitchen", "containers", "organization"],
                "target_demographic": "homemakers",
                "seasonal_pattern": "spring_peak"
            },
            {
                "name": "Measuring Cups Set",
                "category": "Home/Kitchen",
                "brand": "OXO",
                "price": 15.99,
                "margin": 0.32,
                "keywords": ["measuring", "cups", "baking", "cooking"],
                "target_demographic": "homemakers",
                "seasonal_pattern": "holiday_peak"
            },
            {
                "name": "Fitness Resistance Bands",
                "category": "Sports/Fitness",
                "brand": "TRX",
                "price": 19.99,
                "margin": 0.45,
                "keywords": ["fitness", "resistance", "workout", "home"],
                "target_demographic": "fitness",
                "seasonal_pattern": "new_year_peak"
            }
        ]
        
        print(f"   🔍 Clustering {len(sample_products)} products...")
        
        # Identify clusters
        clustering_results = self.identify_product_clusters(sample_products)
        
        print("   🎯 Analyzing bundling opportunities...")
        bundling_analysis = self.analyze_bundling_opportunities(clustering_results)
        
        # Generate cross-sell recommendations for first product
        print("   🔗 Generating cross-sell recommendations...")
        cross_sell_example = self.generate_cross_sell_recommendations(
            sample_products[0], sample_products[1:]
        )
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "ai_system": "ProductClusterAI",
                "version": "1.0.0",
                "products_analyzed": len(sample_products)
            },
            "executive_summary": {
                "total_products": clustering_results["total_products"],
                "clusters_identified": clustering_results["total_clusters"],
                "products_clustered": clustering_results["clustered_products"],
                "clustering_efficiency": round(clustering_results["clustering_efficiency"] * 100, 1),
                "bundling_opportunities": bundling_analysis["total_opportunities"],
                "high_potential_bundles": bundling_analysis["high_potential"],
                "recommendation": self._get_overall_clustering_recommendation(clustering_results, bundling_analysis)
            },
            "clustering_analysis": clustering_results,
            "bundling_opportunities": bundling_analysis,
            "cross_sell_example": {
                "base_product": sample_products[0]["name"],
                "recommendations": cross_sell_example[:5]
            },
            "clustering_algorithms": self.clustering_algorithms
        }
        
        # Save report
        report_file = self.reports_dir / f"product_clustering_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ ProductCluster AI: Analysis completed!")
        print(f"   📦 Products analyzed: {len(sample_products)}")
        print(f"   🔗 Clusters identified: {clustering_results['total_clusters']}")
        print(f"   📈 Bundling opportunities: {bundling_analysis['total_opportunities']}")
        print(f"   ⭐ High-potential bundles: {bundling_analysis['high_potential']}")
        print(f"   📄 Full Report: {report_file}")
        
        # Print top bundling opportunity
        if bundling_analysis["opportunities"]:
            top_bundle = bundling_analysis["opportunities"][0]
            print(f"\n🎯 Top Bundle Opportunity:")
            print(f"   Products: {', '.join([p['name'] for p in top_bundle['products']])}")
            print(f"   Bundle Score: {top_bundle['bundle_score']}")
            print(f"   Customer Savings: ${top_bundle['pricing']['customer_savings']}")
            print(f"   {top_bundle['recommendation']}")
        
        print("🔗 [ProductCluster AI] Ready for product relationship optimization!")
        return report
    
    def _get_overall_clustering_recommendation(self, clustering_results: Dict[str, Any], 
                                            bundling_analysis: Dict[str, Any]) -> str:
        """Generate overall recommendation"""
        efficiency = clustering_results["clustering_efficiency"]
        high_potential = bundling_analysis["high_potential"]
        total_opportunities = bundling_analysis["total_opportunities"]
        
        if efficiency > 0.7 and high_potential >= 2:
            return "EXCELLENT: Strong clustering with multiple high-potential bundling opportunities"
        elif efficiency > 0.5 and total_opportunities >= 2:
            return "GOOD: Solid clustering results with viable bundling options"
        elif efficiency > 0.3 or total_opportunities >= 1:
            return "FAIR: Some clustering potential with limited bundling opportunities"
        else:
            return "POOR: Limited clustering potential, consider expanding product range"

def run():
    """CLI entry point"""
    cluster_ai = ProductClusterAI()
    cluster_ai.run()

if __name__ == "__main__":
    run()
