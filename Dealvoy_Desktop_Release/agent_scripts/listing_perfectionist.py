#!/usr/bin/env python3
"""
ListingPerfectionist Agent
Amazon listing optimization and perfection agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List
import re

class ListingPerfectionist:
    """AI agent for perfecting Amazon product listings"""
    
    def __init__(self):
        self.agent_name = "ListingPerfectionist"
        self.version = "1.0.0"
        self.status = "active"
        self.optimization_areas = ["title", "bullets", "description", "keywords", "images"]
        
    def analyze_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive analysis of product listing"""
        try:
            analysis_results = {}
            
            # Analyze each component
            if "title" in listing_data:
                analysis_results["title"] = self._analyze_title(listing_data["title"])
            
            if "bullet_points" in listing_data:
                analysis_results["bullets"] = self._analyze_bullets(listing_data["bullet_points"])
            
            if "description" in listing_data:
                analysis_results["description"] = self._analyze_description(listing_data["description"])
            
            if "keywords" in listing_data:
                analysis_results["keywords"] = self._analyze_keywords(listing_data["keywords"])
            
            if "images" in listing_data:
                analysis_results["images"] = self._analyze_images(listing_data["images"])
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(analysis_results)
            
            # Generate improvement recommendations
            recommendations = self._generate_recommendations(analysis_results)
            
            result = {
                "asin": listing_data.get("asin", "Unknown"),
                "analysis_results": analysis_results,
                "overall_score": overall_score,
                "grade": self._assign_grade(overall_score),
                "recommendations": recommendations,
                "priority_fixes": self._prioritize_fixes(analysis_results),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"ListingPerfectionist analyzed listing: {overall_score}/100")
            return result
            
        except Exception as e:
            logging.error(f"Listing analysis failed: {e}")
            return {"error": str(e)}
    
    def optimize_title(self, title_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize product title for maximum impact"""
        try:
            current_title = title_data.get("title", "")
            category = title_data.get("category", "")
            keywords = title_data.get("target_keywords", [])
            
            # Analyze current title
            current_analysis = self._analyze_title(current_title)
            
            # Generate optimized versions
            optimized_titles = []
            
            # Version 1: Keyword-optimized
            keyword_title = self._create_keyword_optimized_title(current_title, keywords, category)
            optimized_titles.append({
                "version": "keyword_optimized",
                "title": keyword_title,
                "focus": "SEO and keyword density",
                "score": self._score_title(keyword_title)
            })
            
            # Version 2: Benefit-focused
            benefit_title = self._create_benefit_focused_title(current_title, keywords, category)
            optimized_titles.append({
                "version": "benefit_focused",
                "title": benefit_title,
                "focus": "Customer benefits and features",
                "score": self._score_title(benefit_title)
            })
            
            # Version 3: Emotional appeal
            emotional_title = self._create_emotional_title(current_title, keywords, category)
            optimized_titles.append({
                "version": "emotional_appeal",
                "title": emotional_title,
                "focus": "Emotional triggers and urgency",
                "score": self._score_title(emotional_title)
            })
            
            # Select best version
            best_title = max(optimized_titles, key=lambda x: x["score"])
            
            result = {
                "current_title": current_title,
                "current_analysis": current_analysis,
                "optimized_versions": optimized_titles,
                "recommended_title": best_title,
                "improvement_score": best_title["score"] - current_analysis["score"],
                "character_optimization": self._optimize_character_usage(best_title["title"])
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Title optimization failed: {e}")
            return {"error": str(e)}
    
    def optimize_bullets(self, bullet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize bullet points for maximum conversion"""
        try:
            current_bullets = bullet_data.get("bullets", [])
            features = bullet_data.get("features", [])
            benefits = bullet_data.get("benefits", [])
            keywords = bullet_data.get("keywords", [])
            
            # Analyze current bullets
            current_analysis = [self._analyze_single_bullet(bullet) for bullet in current_bullets]
            
            # Generate optimized bullets
            optimized_bullets = []
            
            # Use feature-benefit framework
            for i in range(5):  # Amazon allows 5 bullets
                if i < len(features):
                    optimized_bullet = self._create_optimized_bullet(
                        features[i], 
                        benefits[i] if i < len(benefits) else "",
                        keywords
                    )
                    optimized_bullets.append(optimized_bullet)
                else:
                    # Generate additional bullets if needed
                    generic_bullet = self._create_generic_bullet(keywords, i)
                    optimized_bullets.append(generic_bullet)
            
            # Calculate improvement
            current_score = sum(analysis["score"] for analysis in current_analysis) / len(current_analysis) if current_analysis else 0
            optimized_score = sum(self._score_bullet(bullet) for bullet in optimized_bullets) / len(optimized_bullets)
            
            result = {
                "current_bullets": current_bullets,
                "current_analysis": current_analysis,
                "optimized_bullets": optimized_bullets,
                "bullet_scores": [self._score_bullet(bullet) for bullet in optimized_bullets],
                "improvement_score": round(optimized_score - current_score, 1),
                "bullet_guidelines": self._get_bullet_guidelines()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Bullet optimization failed: {e}")
            return {"error": str(e)}
    
    def optimize_description(self, description_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize product description with HTML formatting"""
        try:
            current_description = description_data.get("description", "")
            keywords = description_data.get("keywords", [])
            features = description_data.get("features", [])
            use_case = description_data.get("use_case", "")
            
            # Analyze current description
            current_analysis = self._analyze_description(current_description)
            
            # Generate optimized description
            optimized_description = self._create_optimized_description(
                features, keywords, use_case
            )
            
            # Add HTML formatting
            html_description = self._add_html_formatting(optimized_description)
            
            result = {
                "current_description": current_description,
                "current_analysis": current_analysis,
                "optimized_description": optimized_description,
                "html_formatted_description": html_description,
                "keyword_density": self._calculate_keyword_density(optimized_description, keywords),
                "readability_score": self._calculate_readability_score(optimized_description),
                "optimization_tips": self._get_description_tips()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Description optimization failed: {e}")
            return {"error": str(e)}
    
    def _analyze_title(self, title: str) -> Dict[str, Any]:
        """Analyze title quality and optimization"""
        length = len(title)
        word_count = len(title.split())
        
        # Check for power words
        power_words = ["premium", "best", "professional", "ultimate", "advanced", "quality"]
        power_word_count = sum(1 for word in power_words if word.lower() in title.lower())
        
        # Check for numbers/specifics
        numbers = len(re.findall(r'\d+', title))
        
        # Calculate score
        score = 0
        score += min(20, length / 5)  # Length score (max 20)
        score += min(15, word_count * 2)  # Word count score (max 15)
        score += min(20, power_word_count * 5)  # Power words (max 20)
        score += min(15, numbers * 7.5)  # Numbers/specifics (max 15)
        score += 30 if 150 <= length <= 200 else 0  # Optimal length bonus
        
        return {
            "score": round(score),
            "length": length,
            "word_count": word_count,
            "power_words": power_word_count,
            "numbers": numbers,
            "optimal_length": 150 <= length <= 200,
            "issues": self._identify_title_issues(title)
        }
    
    def _analyze_bullets(self, bullets: List[str]) -> Dict[str, Any]:
        """Analyze bullet points quality"""
        if not bullets:
            return {"score": 0, "issues": ["No bullet points provided"]}
        
        bullet_analyses = [self._analyze_single_bullet(bullet) for bullet in bullets]
        avg_score = sum(analysis["score"] for analysis in bullet_analyses) / len(bullet_analyses)
        
        return {
            "score": round(avg_score),
            "bullet_count": len(bullets),
            "individual_scores": [analysis["score"] for analysis in bullet_analyses],
            "issues": [issue for analysis in bullet_analyses for issue in analysis["issues"]]
        }
    
    def _analyze_single_bullet(self, bullet: str) -> Dict[str, Any]:
        """Analyze a single bullet point"""
        length = len(bullet)
        starts_with_caps = bullet[0].isupper() if bullet else False
        has_benefit = any(word in bullet.lower() for word in ["improve", "reduce", "increase", "enhance", "save"])
        
        score = 0
        score += min(30, length / 5)  # Length score
        score += 15 if starts_with_caps else 0  # Capitalization
        score += 20 if has_benefit else 0  # Benefit-focused
        score += 35 if 100 <= length <= 255 else 0  # Optimal length
        
        issues = []
        if length < 50:
            issues.append("Too short")
        if length > 255:
            issues.append("Too long")
        if not starts_with_caps:
            issues.append("Should start with capital letter")
        if not has_benefit:
            issues.append("Should include customer benefit")
        
        return {
            "score": round(score),
            "length": length,
            "issues": issues
        }
    
    def _analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze product description"""
        length = len(description)
        word_count = len(description.split())
        paragraph_count = len(description.split('\n\n'))
        
        # Check for HTML tags
        has_html = bool(re.search(r'<[^>]+>', description))
        
        score = 0
        score += min(25, length / 40)  # Length score
        score += min(20, word_count / 5)  # Word count
        score += min(15, paragraph_count * 5)  # Structure
        score += 20 if has_html else 0  # HTML formatting
        score += 20 if 500 <= length <= 2000 else 0  # Optimal length
        
        return {
            "score": round(score),
            "length": length,
            "word_count": word_count,
            "paragraph_count": paragraph_count,
            "has_html": has_html,
            "issues": self._identify_description_issues(description)
        }
    
    def _analyze_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """Analyze keyword strategy"""
        if not keywords:
            return {"score": 0, "issues": ["No keywords provided"]}
        
        keyword_count = len(keywords)
        avg_length = sum(len(kw) for kw in keywords) / len(keywords)
        long_tail_count = sum(1 for kw in keywords if len(kw.split()) > 2)
        
        score = 0
        score += min(30, keyword_count * 2)  # Keyword quantity
        score += min(25, avg_length)  # Keyword quality
        score += min(25, long_tail_count * 5)  # Long-tail keywords
        score += 20 if 10 <= keyword_count <= 25 else 0  # Optimal count
        
        return {
            "score": round(score),
            "keyword_count": keyword_count,
            "avg_length": round(avg_length, 1),
            "long_tail_count": long_tail_count,
            "suggestions": self._suggest_keyword_improvements(keywords)
        }
    
    def _analyze_images(self, images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze image quality and optimization"""
        if not images:
            return {"score": 0, "issues": ["No images provided"]}
        
        image_count = len(images)
        main_image_quality = images[0].get("quality", "medium") if images else "low"
        lifestyle_images = sum(1 for img in images if img.get("type") == "lifestyle")
        
        score = 0
        score += min(20, image_count * 2.5)  # Image quantity
        score += 25 if main_image_quality == "high" else 10  # Main image quality
        score += min(25, lifestyle_images * 8)  # Lifestyle images
        score += 30 if image_count >= 7 else 0  # Optimal count
        
        return {
            "score": round(score),
            "image_count": image_count,
            "main_image_quality": main_image_quality,
            "lifestyle_images": lifestyle_images,
            "recommendations": self._get_image_recommendations(images)
        }
    
    def _create_keyword_optimized_title(self, current: str, keywords: List[str], category: str) -> str:
        """Create keyword-optimized title"""
        primary_keywords = keywords[:3] if keywords else ["Quality", "Premium", "Best"]
        
        # Structure: Brand + Primary Keywords + Category + Key Feature
        optimized = f"Premium {primary_keywords[0]} {category}"
        if len(primary_keywords) > 1:
            optimized += f" - {primary_keywords[1]} {primary_keywords[2] if len(primary_keywords) > 2 else 'Design'}"
        
        # Ensure under 200 characters
        return optimized[:200]
    
    def _create_benefit_focused_title(self, current: str, keywords: List[str], category: str) -> str:
        """Create benefit-focused title"""
        benefits = ["Improves Performance", "Saves Time", "Increases Efficiency", "Enhances Quality"]
        primary_benefit = benefits[0]
        
        # Structure: Benefit + Product + Feature + Category
        optimized = f"{primary_benefit} - Professional {category}"
        if keywords:
            optimized += f" with {keywords[0]} Technology"
        
        return optimized[:200]
    
    def _create_emotional_title(self, current: str, keywords: List[str], category: str) -> str:
        """Create emotionally appealing title"""
        emotional_triggers = ["Ultimate", "Revolutionary", "Game-Changing", "Professional-Grade"]
        trigger = emotional_triggers[0]
        
        # Structure: Emotional Trigger + Category + Benefit Promise
        optimized = f"{trigger} {category} - Transform Your Experience"
        if keywords:
            optimized += f" with Advanced {keywords[0]}"
        
        return optimized[:200]
    
    def _score_title(self, title: str) -> int:
        """Score a title based on optimization criteria"""
        return self._analyze_title(title)["score"]
    
    def _create_optimized_bullet(self, feature: str, benefit: str, keywords: List[str]) -> str:
        """Create optimized bullet point using feature-benefit framework"""
        if not feature:
            feature = "Advanced Technology"
        if not benefit:
            benefit = "enhances your experience"
        
        # Structure: FEATURE - Benefit with keyword integration
        keyword_integration = f" ({keywords[0]})" if keywords else ""
        bullet = f"✓ {feature.upper()} - {benefit.capitalize()}{keyword_integration} for superior performance and reliability."
        
        return bullet[:255]  # Amazon limit
    
    def _create_generic_bullet(self, keywords: List[str], index: int) -> str:
        """Create generic bullet when specific features aren't available"""
        generic_bullets = [
            "PREMIUM QUALITY - Engineered with precision for long-lasting durability and optimal performance.",
            "EASY TO USE - Simple installation and operation, perfect for both beginners and professionals.",
            "VERSATILE DESIGN - Suitable for multiple applications and environments, maximizing value.",
            "SATISFACTION GUARANTEED - Backed by our commitment to quality and customer satisfaction."
        ]
        
        base_bullet = generic_bullets[index % len(generic_bullets)]
        if keywords:
            base_bullet = base_bullet.replace("PREMIUM", keywords[0].upper())
        
        return base_bullet
    
    def _score_bullet(self, bullet: str) -> int:
        """Score a bullet point"""
        return self._analyze_single_bullet(bullet)["score"]
    
    def _create_optimized_description(self, features: List[str], keywords: List[str], use_case: str) -> str:
        """Create optimized product description"""
        sections = []
        
        # Opening hook
        sections.append(f"Transform your {use_case or 'experience'} with our premium solution.")
        
        # Key features section
        if features:
            sections.append("KEY FEATURES:")
            for feature in features[:5]:
                sections.append(f"• {feature}")
        
        # Benefits section
        sections.append("BENEFITS:")
        sections.append("• Enhanced performance and reliability")
        sections.append("• Easy to use and maintain")
        sections.append("• Professional-grade quality")
        
        # Keyword integration
        if keywords:
            keyword_text = f"Our {keywords[0]} technology ensures optimal results."
            sections.append(keyword_text)
        
        # Call to action
        sections.append("Order now and experience the difference!")
        
        return "\n\n".join(sections)
    
    def _add_html_formatting(self, description: str) -> str:
        """Add HTML formatting to description"""
        # Convert to HTML with basic formatting
        html_desc = description.replace("\n\n", "</p><p>")
        html_desc = f"<p>{html_desc}</p>"
        
        # Add formatting for key sections
        html_desc = html_desc.replace("KEY FEATURES:", "<b>KEY FEATURES:</b>")
        html_desc = html_desc.replace("BENEFITS:", "<b>BENEFITS:</b>")
        html_desc = html_desc.replace("•", "<br>•")
        
        return html_desc
    
    def _calculate_overall_score(self, analysis: Dict) -> int:
        """Calculate overall listing score"""
        scores = []
        weights = {"title": 0.25, "bullets": 0.25, "description": 0.2, "keywords": 0.15, "images": 0.15}
        
        for area, weight in weights.items():
            if area in analysis and "score" in analysis[area]:
                scores.append(analysis[area]["score"] * weight)
        
        return round(sum(scores)) if scores else 0
    
    def _assign_grade(self, score: int) -> str:
        """Assign letter grade based on score"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        for area, data in analysis.items():
            if "score" in data and data["score"] < 70:
                recommendations.append(f"Improve {area} optimization (current score: {data['score']}/100)")
        
        return recommendations
    
    def _prioritize_fixes(self, analysis: Dict) -> List[str]:
        """Prioritize fixes by impact"""
        fixes = []
        
        # Sort by score (lowest first)
        sorted_areas = sorted(analysis.items(), key=lambda x: x[1].get("score", 0))
        
        for area, data in sorted_areas[:3]:  # Top 3 priorities
            fixes.append(f"{area.title()} optimization (Score: {data.get('score', 0)}/100)")
        
        return fixes
    
    def _identify_title_issues(self, title: str) -> List[str]:
        """Identify specific title issues"""
        issues = []
        
        if len(title) < 80:
            issues.append("Title too short - missing keyword opportunities")
        if len(title) > 200:
            issues.append("Title too long - may be truncated")
        if not any(char.isdigit() for char in title):
            issues.append("Consider adding specific numbers or quantities")
        
        return issues
    
    def _identify_description_issues(self, description: str) -> List[str]:
        """Identify description issues"""
        issues = []
        
        if len(description) < 200:
            issues.append("Description too short")
        if not re.search(r'<[^>]+>', description):
            issues.append("Missing HTML formatting")
        if description.count('\n') < 2:
            issues.append("Poor paragraph structure")
        
        return issues
    
    def _suggest_keyword_improvements(self, keywords: List[str]) -> List[str]:
        """Suggest keyword improvements"""
        suggestions = []
        
        if len(keywords) < 10:
            suggestions.append("Add more target keywords")
        
        long_tail = sum(1 for kw in keywords if len(kw.split()) > 2)
        if long_tail < len(keywords) * 0.3:
            suggestions.append("Include more long-tail keywords")
        
        return suggestions
    
    def _get_image_recommendations(self, images: List[Dict]) -> List[str]:
        """Get image optimization recommendations"""
        recommendations = []
        
        if len(images) < 7:
            recommendations.append("Add more product images (aim for 7-9)")
        
        lifestyle_count = sum(1 for img in images if img.get("type") == "lifestyle")
        if lifestyle_count < 2:
            recommendations.append("Add lifestyle/in-use images")
        
        return recommendations
    
    def _optimize_character_usage(self, title: str) -> Dict[str, Any]:
        """Optimize character usage in title"""
        return {
            "current_length": len(title),
            "optimal_range": "150-200 characters",
            "remaining_chars": 200 - len(title),
            "usage_percentage": round((len(title) / 200) * 100, 1)
        }
    
    def _get_bullet_guidelines(self) -> List[str]:
        """Get bullet point guidelines"""
        return [
            "Start each bullet with a benefit or feature",
            "Use 100-255 characters per bullet",
            "Include relevant keywords naturally",
            "Focus on customer benefits, not just features",
            "Use strong action words and descriptive language"
        ]
    
    def _calculate_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density in text"""
        word_count = len(text.split())
        densities = {}
        
        for keyword in keywords[:5]:  # Top 5 keywords
            count = text.lower().count(keyword.lower())
            density = (count / word_count) * 100 if word_count > 0 else 0
            densities[keyword] = round(density, 2)
        
        return densities
    
    def _calculate_readability_score(self, text: str) -> int:
        """Calculate basic readability score"""
        words = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        if sentences == 0:
            return 50
        
        avg_words_per_sentence = words / sentences
        
        # Simple readability score (higher is better)
        if avg_words_per_sentence <= 15:
            return 90
        elif avg_words_per_sentence <= 20:
            return 75
        elif avg_words_per_sentence <= 25:
            return 60
        else:
            return 40
    
    def _get_description_tips(self) -> List[str]:
        """Get description optimization tips"""
        return [
            "Use HTML formatting for better readability",
            "Include customer benefits in every section",
            "Maintain 2-3% keyword density",
            "Structure with clear headings and bullet points",
            "End with a strong call-to-action"
        ]
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        optimization_type = input_data.get("optimization_type", "analyze")
        
        if optimization_type == "analyze" and "listing_data" in input_data:
            return self.analyze_listing(input_data["listing_data"])
        elif optimization_type == "title" and "title_data" in input_data:
            return self.optimize_title(input_data["title_data"])
        elif optimization_type == "bullets" and "bullet_data" in input_data:
            return self.optimize_bullets(input_data["bullet_data"])
        elif optimization_type == "description" and "description_data" in input_data:
            return self.optimize_description(input_data["description_data"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["listing_analysis", "title_optimization", "bullet_optimization", "description_optimization"],
            "optimization_areas": self.optimization_areas
        }

if __name__ == "__main__":
    agent = ListingPerfectionist()
    print(json.dumps(agent.run(), indent=2))
