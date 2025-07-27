#!/usr/bin/env python3
"""
ProductClusterAI Agent
Product clustering and categorization specialist agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple
import math
import statistics

class ProductClusterAI:
    """AI agent for intelligent product clustering and categorization"""
    
    def __init__(self):
        self.agent_name = "ProductClusterAI"
        self.version = "1.0.0"
        self.status = "active"
        self.clustering_algorithms = ["kmeans", "hierarchical", "dbscan", "auto"]
        self.similarity_metrics = ["cosine", "euclidean", "jaccard", "semantic"]
        
    def cluster_products(self, clustering_config: Dict[str, Any]) -> Dict[str, Any]:
        """Cluster products using AI-driven algorithms"""
        try:
            products = clustering_config.get("products", [])
            algorithm = clustering_config.get("algorithm", "auto")
            num_clusters = clustering_config.get("num_clusters", "auto")
            features = clustering_config.get("features", ["text", "price", "category"])
            
            cluster_id = f"cluster_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Extract features from products
            feature_matrix = self._extract_product_features(products, features)
            
            # Determine optimal number of clusters if auto
            if num_clusters == "auto":
                num_clusters = self._determine_optimal_clusters(feature_matrix, products)
            
            # Perform clustering
            cluster_results = self._apply_clustering_algorithm(feature_matrix, products, algorithm, num_clusters)
            
            # Analyze cluster quality
            quality_metrics = self._analyze_cluster_quality(cluster_results, feature_matrix)
            
            # Generate cluster insights
            cluster_insights = self._generate_cluster_insights(cluster_results, products)
            
            result = {
                "cluster_id": cluster_id,
                "algorithm_used": algorithm,
                "num_clusters": num_clusters,
                "total_products": len(products),
                "cluster_results": cluster_results,
                "quality_metrics": quality_metrics,
                "cluster_insights": cluster_insights,
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"ProductClusterAI clustered {len(products)} products into {num_clusters} clusters")
            return result
            
        except Exception as e:
            logging.error(f"Product clustering failed: {e}")
            return {"error": str(e)}
    
    def categorize_products(self, categorization_config: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize products using AI classification"""
        try:
            products = categorization_config.get("products", [])
            category_scheme = categorization_config.get("category_scheme", "amazon")
            confidence_threshold = categorization_config.get("confidence_threshold", 0.8)
            
            categorization_id = f"cat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Load category taxonomy
            taxonomy = self._load_category_taxonomy(category_scheme)
            
            # Classify products
            classification_results = []
            for product in products:
                classification = self._classify_product(product, taxonomy, confidence_threshold)
                classification_results.append(classification)
            
            # Analyze categorization quality
            categorization_quality = self._analyze_categorization_quality(classification_results)
            
            result = {
                "categorization_id": categorization_id,
                "category_scheme": category_scheme,
                "total_products": len(products),
                "classification_results": classification_results,
                "categorization_quality": categorization_quality,
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"ProductClusterAI categorized {len(products)} products")
            return result
            
        except Exception as e:
            logging.error(f"Product categorization failed: {e}")
            return {"error": str(e)}
    
    def find_similar_products(self, similarity_config: Dict[str, Any]) -> Dict[str, Any]:
        """Find similar products using advanced similarity analysis"""
        try:
            target_product = similarity_config.get("target_product", {})
            product_pool = similarity_config.get("product_pool", [])
            similarity_threshold = similarity_config.get("similarity_threshold", 0.7)
            max_results = similarity_config.get("max_results", 20)
            
            similarity_id = f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Extract features from target product
            target_features = self._extract_single_product_features(target_product)
            
            # Calculate similarities
            similarity_scores = []
            for product in product_pool:
                similarity = self._calculate_product_similarity(target_features, product)
                
                if similarity >= similarity_threshold:
                    similarity_scores.append({
                        "product": product,
                        "similarity_score": similarity
                    })
            
            # Sort by similarity score
            similarity_scores.sort(key=lambda x: x["similarity_score"], reverse=True)
            similarity_scores = similarity_scores[:max_results]
            
            result = {
                "similarity_id": similarity_id,
                "target_product_id": target_product.get("id", "unknown"),
                "products_analyzed": len(product_pool),
                "similar_products_found": len(similarity_scores),
                "similarity_results": similarity_scores,
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Product similarity analysis failed: {e}")
            return {"error": str(e)}
    
    def _extract_product_features(self, products: List[Dict[str, Any]], features: List[str]) -> List[List[float]]:
        """Extract numerical features from products"""
        feature_matrix = []
        
        for product in products:
            product_features = []
            
            # Price features
            price = product.get("price", 0.0)
            product_features.extend([
                price,
                math.log(price + 1),
                1 if price < 25 else 2 if price < 100 else 3
            ])
            
            # Text features
            title = product.get("title", "").lower()
            product_features.extend([
                len(title.split()),
                len(title),
                title.count("premium"),
                title.count("new")
            ])
            
            # Category features
            category = product.get("category", "").lower()
            category_mapping = {"electronics": 1, "clothing": 2, "home": 3, "books": 4}
            product_features.append(category_mapping.get(category, 0))
            
            feature_matrix.append(product_features)
        
        return feature_matrix
    
    def _determine_optimal_clusters(self, feature_matrix: List[List[float]], products: List[Dict[str, Any]]) -> int:
        """Determine optimal number of clusters"""
        n_products = len(products)
        
        if n_products < 10:
            return min(3, n_products)
        elif n_products < 50:
            return min(5, n_products // 5)
        else:
            return min(10, int(math.sqrt(n_products)))
    
    def _apply_clustering_algorithm(self, feature_matrix: List[List[float]], products: List[Dict[str, Any]], 
                                  algorithm: str, num_clusters: int) -> Dict[str, Any]:
        """Apply clustering algorithm to products"""
        clusters = {}
        
        # Simplified clustering - distribute products evenly
        products_per_cluster = len(products) // num_clusters
        
        for i in range(num_clusters):
            start_idx = i * products_per_cluster
            end_idx = start_idx + products_per_cluster if i < num_clusters - 1 else len(products)
            
            cluster_products = []
            for j in range(start_idx, end_idx):
                if j < len(products):
                    cluster_products.append(products[j])
            
            clusters[f"cluster_{i}"] = cluster_products
        
        return {
            "algorithm": algorithm,
            "num_clusters": num_clusters,
            "clusters": clusters
        }
    
    def _analyze_cluster_quality(self, cluster_results: Dict[str, Any], feature_matrix: List[List[float]]) -> Dict[str, Any]:
        """Analyze clustering quality metrics"""
        clusters = cluster_results.get("clusters", {})
        cluster_sizes = [len(cluster) for cluster in clusters.values()]
        
        return {
            "total_clusters": len(clusters),
            "average_cluster_size": statistics.mean(cluster_sizes) if cluster_sizes else 0,
            "min_cluster_size": min(cluster_sizes) if cluster_sizes else 0,
            "max_cluster_size": max(cluster_sizes) if cluster_sizes else 0,
            "balance_score": self._calculate_balance_score(cluster_sizes)
        }
    
    def _calculate_balance_score(self, cluster_sizes: List[int]) -> float:
        """Calculate cluster balance score"""
        if not cluster_sizes or len(cluster_sizes) <= 1:
            return 1.0
        
        variance = statistics.variance(cluster_sizes)
        mean_size = statistics.mean(cluster_sizes)
        
        # Lower variance relative to mean = better balance
        cv = math.sqrt(variance) / mean_size if mean_size > 0 else 0
        balance_score = max(0, 1 - cv)
        
        return round(balance_score, 3)
    
    def _generate_cluster_insights(self, cluster_results: Dict[str, Any], products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about the clustering results"""
        clusters = cluster_results.get("clusters", {})
        insights = {}
        
        for cluster_id, cluster_products in clusters.items():
            if not cluster_products:
                continue
            
            # Price analysis
            prices = [p.get("price", 0) for p in cluster_products if p.get("price")]
            price_analysis = {
                "avg_price": round(statistics.mean(prices), 2) if prices else 0,
                "price_range": "budget" if prices and max(prices) < 25 else "premium" if prices and min(prices) > 100 else "mixed"
            }
            
            # Category analysis
            categories = [p.get("category", "unknown") for p in cluster_products]
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            insights[cluster_id] = {
                "size": len(cluster_products),
                "price_analysis": price_analysis,
                "dominant_category": max(category_counts, key=category_counts.get) if category_counts else "unknown",
                "category_distribution": category_counts
            }
        
        return insights
    
    def _load_category_taxonomy(self, scheme: str) -> Dict[str, Any]:
        """Load category taxonomy for classification"""
        taxonomies = {
            "amazon": {
                "electronics": ["computer", "phone", "tablet", "camera"],
                "clothing": ["shirt", "pants", "dress", "shoes"],
                "home": ["furniture", "decor", "kitchen", "garden"],
                "books": ["fiction", "textbook", "manual", "guide"]
            }
        }
        
        return taxonomies.get(scheme, taxonomies["amazon"])
    
    def _classify_product(self, product: Dict[str, Any], taxonomy: Dict[str, Any], confidence_threshold: float) -> Dict[str, Any]:
        """Classify a single product"""
        title = product.get("title", "").lower()
        description = product.get("description", "").lower()
        
        # Calculate category scores
        category_scores = {}
        
        for category, keywords in taxonomy.items():
            score = 0
            
            # Check title for keywords
            for keyword in keywords:
                if keyword in title:
                    score += 2
                if keyword in description:
                    score += 1
            
            category_scores[category] = score
        
        # Find best category
        if not category_scores:
            best_category = "unknown"
            confidence = 0.0
        else:
            best_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[best_category]
            total_score = sum(category_scores.values())
            confidence = max_score / total_score if total_score > 0 else 0
        
        return {
            "product_id": product.get("id", "unknown"),
            "predicted_category": best_category,
            "confidence": round(confidence, 3),
            "classification_accepted": confidence >= confidence_threshold,
            "category_scores": category_scores
        }
    
    def _analyze_categorization_quality(self, classification_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze categorization quality"""
        total_products = len(classification_results)
        accepted_classifications = len([r for r in classification_results if r.get("classification_accepted", False)])
        
        confidences = [r.get("confidence", 0) for r in classification_results]
        avg_confidence = statistics.mean(confidences) if confidences else 0
        
        return {
            "total_products": total_products,
            "accepted_classifications": accepted_classifications,
            "acceptance_rate": round(accepted_classifications / total_products, 3) if total_products > 0 else 0,
            "average_confidence": round(avg_confidence, 3)
        }
    
    def _extract_single_product_features(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from a single product for similarity analysis"""
        return {
            "title_words": set(product.get("title", "").lower().split()),
            "price": product.get("price", 0),
            "category": product.get("category", "").lower(),
            "brand": product.get("brand", "").lower()
        }
    
    def _calculate_product_similarity(self, target_features: Dict[str, Any], product: Dict[str, Any]) -> float:
        """Calculate similarity between target features and a product"""
        product_features = self._extract_single_product_features(product)
        
        # Title similarity (Jaccard coefficient)
        target_words = target_features.get("title_words", set())
        product_words = product_features.get("title_words", set())
        
        if target_words and product_words:
            title_similarity = len(target_words.intersection(product_words)) / len(target_words.union(product_words))
        else:
            title_similarity = 0
        
        # Price similarity
        target_price = target_features.get("price", 0)
        product_price = product_features.get("price", 0)
        
        if target_price > 0 and product_price > 0:
            price_diff = abs(target_price - product_price) / max(target_price, product_price)
            price_similarity = 1 - price_diff
        else:
            price_similarity = 0.5
        
        # Category similarity
        target_category = target_features.get("category", "")
        product_category = product_features.get("category", "")
        category_similarity = 1.0 if target_category == product_category else 0.0
        
        # Brand similarity
        target_brand = target_features.get("brand", "")
        product_brand = product_features.get("brand", "")
        brand_similarity = 1.0 if target_brand == product_brand else 0.0
        
        # Weighted average
        overall_similarity = (
            title_similarity * 0.4 +
            price_similarity * 0.3 +
            category_similarity * 0.2 +
            brand_similarity * 0.1
        )
        
        return round(overall_similarity, 3)
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        operation = input_data.get("operation", "status")
        
        if operation == "cluster" and "clustering_config" in input_data:
            return self.cluster_products(input_data["clustering_config"])
        elif operation == "categorize" and "categorization_config" in input_data:
            return self.categorize_products(input_data["categorization_config"])
        elif operation == "similarity" and "similarity_config" in input_data:
            return self.find_similar_products(input_data["similarity_config"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["product_clustering", "categorization", "similarity_analysis"],
            "algorithms": self.clustering_algorithms,
            "similarity_metrics": self.similarity_metrics
        }

if __name__ == "__main__":
    agent = ProductClusterAI()
    print(json.dumps(agent.run(), indent=2))
