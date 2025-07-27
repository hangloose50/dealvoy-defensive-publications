#!/usr/bin/env python3
"""
PromptTuner Agent
AI prompt optimization and tuning specialist agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional
import time
import random
import re

class PromptTuner:
    """AI agent for optimizing and tuning prompts for better AI performance"""
    
    def __init__(self):
        self.agent_name = "PromptTuner"
        self.version = "1.0.0"
        self.status = "active"
        self.optimization_strategies = ["clarity", "specificity", "context", "examples", "structure", "constraints"]
        self.prompt_types = ["instruction", "question", "completion", "conversation", "classification", "extraction"]
        self.evaluation_metrics = ["relevance", "accuracy", "completeness", "clarity", "efficiency"]
        
    def analyze_prompt_performance(self, analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current prompt performance and identify optimization opportunities"""
        try:
            prompts = analysis_config.get("prompts", [])
            test_cases = analysis_config.get("test_cases", [])
            evaluation_criteria = analysis_config.get("evaluation_criteria", self.evaluation_metrics)
            baseline_metrics = analysis_config.get("baseline_metrics", {})
            
            analysis_id = f"prompt_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyze each prompt
            prompt_analyses = []
            
            for idx, prompt in enumerate(prompts):
                prompt_id = prompt.get("id", f"prompt_{idx}")
                prompt_text = prompt.get("text", "")
                prompt_type = prompt.get("type", "instruction")
                
                # Perform comprehensive prompt analysis
                structural_analysis = self._analyze_prompt_structure(prompt_text, prompt_type)
                clarity_analysis = self._analyze_prompt_clarity(prompt_text)
                specificity_analysis = self._analyze_prompt_specificity(prompt_text)
                context_analysis = self._analyze_prompt_context(prompt_text)
                
                # Evaluate against test cases
                test_performance = self._evaluate_prompt_against_tests(prompt, test_cases)
                
                # Calculate performance metrics
                performance_metrics = self._calculate_prompt_metrics(
                    structural_analysis, clarity_analysis, specificity_analysis, 
                    context_analysis, test_performance
                )
                
                # Identify optimization opportunities
                optimization_opportunities = self._identify_optimization_opportunities(
                    structural_analysis, clarity_analysis, specificity_analysis, context_analysis
                )
                
                # Generate improvement suggestions
                improvement_suggestions = self._generate_improvement_suggestions(
                    prompt_text, prompt_type, optimization_opportunities
                )
                
                prompt_analysis = {
                    "prompt_id": prompt_id,
                    "prompt_type": prompt_type,
                    "original_prompt": prompt_text,
                    "structural_analysis": structural_analysis,
                    "clarity_analysis": clarity_analysis,
                    "specificity_analysis": specificity_analysis,
                    "context_analysis": context_analysis,
                    "test_performance": test_performance,
                    "performance_metrics": performance_metrics,
                    "optimization_opportunities": optimization_opportunities,
                    "improvement_suggestions": improvement_suggestions
                }
                
                prompt_analyses.append(prompt_analysis)
            
            # Generate overall analysis summary
            overall_summary = self._generate_analysis_summary(prompt_analyses)
            
            # Compare against baselines
            baseline_comparison = self._compare_against_baselines(prompt_analyses, baseline_metrics)
            
            # Generate strategic recommendations
            strategic_recommendations = self._generate_strategic_recommendations(
                prompt_analyses, overall_summary
            )
            
            result = {
                "analysis_id": analysis_id,
                "total_prompts_analyzed": len(prompts),
                "evaluation_criteria": evaluation_criteria,
                "prompt_analyses": prompt_analyses,
                "overall_summary": overall_summary,
                "baseline_comparison": baseline_comparison,
                "strategic_recommendations": strategic_recommendations,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"PromptTuner analyzed {len(prompts)} prompts with {len(strategic_recommendations)} recommendations")
            return result
            
        except Exception as e:
            logging.error(f"Prompt performance analysis failed: {e}")
            return {"error": str(e)}
    
    def optimize_prompts(self, optimization_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize prompts using various enhancement strategies"""
        try:
            prompts = optimization_config.get("prompts", [])
            optimization_strategies = optimization_config.get("strategies", self.optimization_strategies)
            target_metrics = optimization_config.get("target_metrics", {})
            test_cases = optimization_config.get("test_cases", [])
            iterations = optimization_config.get("iterations", 3)
            
            optimization_id = f"prompt_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Optimize each prompt
            optimization_results = []
            
            for idx, prompt in enumerate(prompts):
                prompt_id = prompt.get("id", f"prompt_{idx}")
                original_text = prompt.get("text", "")
                prompt_type = prompt.get("type", "instruction")
                
                # Track optimization iterations
                optimization_iterations = []
                current_prompt = original_text
                
                for iteration in range(iterations):
                    # Apply optimization strategies
                    optimized_versions = {}
                    
                    for strategy in optimization_strategies:
                        optimized_prompt = self._apply_optimization_strategy(
                            current_prompt, strategy, prompt_type
                        )
                        optimized_versions[strategy] = optimized_prompt
                    
                    # Evaluate optimized versions
                    strategy_evaluations = {}
                    
                    for strategy, optimized_prompt in optimized_versions.items():
                        evaluation = self._evaluate_optimized_prompt(
                            original_text, optimized_prompt, test_cases, target_metrics
                        )
                        strategy_evaluations[strategy] = evaluation
                    
                    # Select best optimization
                    best_strategy = self._select_best_optimization(strategy_evaluations)
                    
                    if best_strategy:
                        current_prompt = optimized_versions[best_strategy]
                        iteration_result = {
                            "iteration": iteration + 1,
                            "applied_strategy": best_strategy,
                            "prompt_version": current_prompt,
                            "improvement_metrics": strategy_evaluations[best_strategy],
                            "all_strategy_results": strategy_evaluations
                        }
                    else:
                        iteration_result = {
                            "iteration": iteration + 1,
                            "applied_strategy": None,
                            "prompt_version": current_prompt,
                            "improvement_metrics": {},
                            "note": "No improvement found in this iteration"
                        }
                    
                    optimization_iterations.append(iteration_result)
                
                # Calculate final optimization results
                final_evaluation = self._evaluate_final_optimization(
                    original_text, current_prompt, test_cases, target_metrics
                )
                
                # Generate optimization insights
                optimization_insights = self._generate_optimization_insights(
                    optimization_iterations, final_evaluation
                )
                
                prompt_optimization = {
                    "prompt_id": prompt_id,
                    "prompt_type": prompt_type,
                    "original_prompt": original_text,
                    "optimized_prompt": current_prompt,
                    "optimization_iterations": optimization_iterations,
                    "final_evaluation": final_evaluation,
                    "optimization_insights": optimization_insights,
                    "total_iterations": iterations,
                    "strategies_applied": optimization_strategies
                }
                
                optimization_results.append(prompt_optimization)
            
            # Generate optimization summary
            optimization_summary = self._generate_optimization_summary(optimization_results)
            
            # Calculate ROI and impact metrics
            impact_analysis = self._calculate_optimization_impact(optimization_results)
            
            # Generate deployment recommendations
            deployment_recommendations = self._generate_deployment_recommendations(
                optimization_results, impact_analysis
            )
            
            result = {
                "optimization_id": optimization_id,
                "total_prompts_optimized": len(prompts),
                "optimization_strategies_used": optimization_strategies,
                "total_iterations": iterations,
                "optimization_results": optimization_results,
                "optimization_summary": optimization_summary,
                "impact_analysis": impact_analysis,
                "deployment_recommendations": deployment_recommendations,
                "optimization_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"PromptTuner optimized {len(prompts)} prompts across {iterations} iterations")
            return result
            
        except Exception as e:
            logging.error(f"Prompt optimization failed: {e}")
            return {"error": str(e)}
    
    def run_ab_tests(self, ab_test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run A/B tests to compare prompt variants"""
        try:
            prompt_variants = ab_test_config.get("prompt_variants", [])
            test_scenarios = ab_test_config.get("test_scenarios", [])
            sample_size = ab_test_config.get("sample_size", 100)
            confidence_level = ab_test_config.get("confidence_level", 0.95)
            success_metrics = ab_test_config.get("success_metrics", ["accuracy", "relevance"])
            
            ab_test_id = f"ab_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Validate test configuration
            if len(prompt_variants) < 2:
                return {"error": "At least 2 prompt variants required for A/B testing"}
            
            # Run A/B test for each metric
            ab_test_results = {}
            
            for metric in success_metrics:
                metric_results = self._run_metric_ab_test(
                    prompt_variants, test_scenarios, sample_size, metric
                )
                ab_test_results[metric] = metric_results
            
            # Calculate statistical significance
            statistical_analysis = self._calculate_statistical_significance(
                ab_test_results, confidence_level
            )
            
            # Identify winning variants
            winning_variants = self._identify_winning_variants(
                ab_test_results, statistical_analysis
            )
            
            # Generate A/B test insights
            ab_test_insights = self._generate_ab_test_insights(
                ab_test_results, statistical_analysis, winning_variants
            )
            
            # Calculate confidence intervals
            confidence_intervals = self._calculate_confidence_intervals(
                ab_test_results, confidence_level
            )
            
            # Generate recommendation for deployment
            deployment_recommendation = self._generate_ab_deployment_recommendation(
                winning_variants, statistical_analysis, confidence_intervals
            )
            
            result = {
                "ab_test_id": ab_test_id,
                "test_configuration": {
                    "total_variants": len(prompt_variants),
                    "sample_size_per_variant": sample_size,
                    "confidence_level": confidence_level,
                    "success_metrics": success_metrics
                },
                "prompt_variants": prompt_variants,
                "ab_test_results": ab_test_results,
                "statistical_analysis": statistical_analysis,
                "winning_variants": winning_variants,
                "confidence_intervals": confidence_intervals,
                "ab_test_insights": ab_test_insights,
                "deployment_recommendation": deployment_recommendation,
                "test_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"PromptTuner completed A/B test with {len(prompt_variants)} variants")
            return result
            
        except Exception as e:
            logging.error(f"A/B testing failed: {e}")
            return {"error": str(e)}
    
    def monitor_prompt_drift(self, monitoring_config: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor prompt performance over time and detect drift"""
        try:
            prompts = monitoring_config.get("prompts", [])
            monitoring_period_days = monitoring_config.get("monitoring_period_days", 30)
            drift_threshold = monitoring_config.get("drift_threshold", 0.1)
            performance_metrics = monitoring_config.get("metrics", ["accuracy", "relevance"])
            
            monitoring_id = f"drift_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Simulate historical performance data
            drift_analysis_results = []
            
            for idx, prompt in enumerate(prompts):
                prompt_id = prompt.get("id", f"prompt_{idx}")
                prompt_text = prompt.get("text", "")
                
                # Generate simulated performance timeline
                performance_timeline = self._generate_performance_timeline(
                    prompt_id, monitoring_period_days, performance_metrics
                )
                
                # Detect drift patterns
                drift_patterns = self._detect_drift_patterns(
                    performance_timeline, drift_threshold
                )
                
                # Analyze drift causes
                drift_causes = self._analyze_drift_causes(drift_patterns, prompt_text)
                
                # Generate drift alerts
                drift_alerts = self._generate_drift_alerts(drift_patterns, drift_threshold)
                
                # Calculate drift severity
                drift_severity = self._calculate_drift_severity(drift_patterns)
                
                # Generate mitigation recommendations
                mitigation_recommendations = self._generate_drift_mitigation(
                    drift_patterns, drift_causes, drift_severity
                )
                
                drift_analysis = {
                    "prompt_id": prompt_id,
                    "monitoring_period_days": monitoring_period_days,
                    "performance_timeline": performance_timeline,
                    "drift_patterns": drift_patterns,
                    "drift_causes": drift_causes,
                    "drift_alerts": drift_alerts,
                    "drift_severity": drift_severity,
                    "mitigation_recommendations": mitigation_recommendations
                }
                
                drift_analysis_results.append(drift_analysis)
            
            # Generate overall drift summary
            overall_drift_summary = self._generate_overall_drift_summary(drift_analysis_results)
            
            # Identify system-wide trends
            system_trends = self._identify_system_trends(drift_analysis_results)
            
            # Generate proactive recommendations
            proactive_recommendations = self._generate_proactive_recommendations(
                overall_drift_summary, system_trends
            )
            
            result = {
                "monitoring_id": monitoring_id,
                "monitoring_configuration": {
                    "total_prompts_monitored": len(prompts),
                    "monitoring_period_days": monitoring_period_days,
                    "drift_threshold": drift_threshold,
                    "performance_metrics": performance_metrics
                },
                "drift_analysis_results": drift_analysis_results,
                "overall_drift_summary": overall_drift_summary,
                "system_trends": system_trends,
                "proactive_recommendations": proactive_recommendations,
                "monitoring_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"PromptTuner monitored drift for {len(prompts)} prompts over {monitoring_period_days} days")
            return result
            
        except Exception as e:
            logging.error(f"Prompt drift monitoring failed: {e}")
            return {"error": str(e)}
    
    def _analyze_prompt_structure(self, prompt_text: str, prompt_type: str) -> Dict[str, Any]:
        """Analyze the structural elements of a prompt"""
        structure_analysis = {
            "length_characters": len(prompt_text),
            "word_count": len(prompt_text.split()),
            "sentence_count": len([s for s in prompt_text.split('.') if s.strip()]),
            "has_clear_instruction": bool(re.search(r'\b(please|can you|help|generate|create|analyze)\b', prompt_text.lower())),
            "has_examples": bool(re.search(r'\b(example|for instance|such as)\b', prompt_text.lower())),
            "has_constraints": bool(re.search(r'\b(must|should|avoid|don\'t|limit)\b', prompt_text.lower())),
            "has_context": bool(re.search(r'\b(given|considering|based on|context)\b', prompt_text.lower())),
            "question_marks": prompt_text.count('?'),
            "exclamation_marks": prompt_text.count('!'),
            "bullet_points": prompt_text.count('•') + prompt_text.count('-'),
            "numbered_items": len(re.findall(r'\d+\.', prompt_text))
        }
        
        # Calculate structure score
        structure_score = 0
        if structure_analysis["has_clear_instruction"]:
            structure_score += 25
        if structure_analysis["has_examples"]:
            structure_score += 20
        if structure_analysis["has_constraints"]:
            structure_score += 20
        if structure_analysis["has_context"]:
            structure_score += 15
        if 50 <= structure_analysis["word_count"] <= 200:  # Optimal length
            structure_score += 20
        
        structure_analysis["structure_score"] = structure_score
        
        return structure_analysis
    
    def _analyze_prompt_clarity(self, prompt_text: str) -> Dict[str, Any]:
        """Analyze the clarity and readability of a prompt"""
        clarity_analysis = {
            "average_word_length": sum(len(word) for word in prompt_text.split()) / len(prompt_text.split()) if prompt_text.split() else 0,
            "complex_words": len([word for word in prompt_text.split() if len(word) > 8]),
            "passive_voice_indicators": len(re.findall(r'\b(was|were|been|being)\s+\w+ed\b', prompt_text.lower())),
            "ambiguous_terms": len(re.findall(r'\b(something|anything|various|different|some|many)\b', prompt_text.lower())),
            "jargon_terms": len(re.findall(r'\b(utilize|facilitate|implement|optimize|leverage)\b', prompt_text.lower())),
            "readability_score": random.uniform(60, 95)  # Simulated readability score
        }
        
        # Calculate clarity score
        clarity_score = 100
        clarity_score -= clarity_analysis["complex_words"] * 2
        clarity_score -= clarity_analysis["passive_voice_indicators"] * 5
        clarity_score -= clarity_analysis["ambiguous_terms"] * 10
        clarity_score -= clarity_analysis["jargon_terms"] * 3
        
        clarity_analysis["clarity_score"] = max(0, clarity_score)
        
        return clarity_analysis
    
    def _analyze_prompt_specificity(self, prompt_text: str) -> Dict[str, Any]:
        """Analyze how specific and detailed the prompt is"""
        specificity_analysis = {
            "specific_nouns": len(re.findall(r'\b[A-Z][a-z]+\b', prompt_text)),  # Proper nouns
            "numbers_and_quantities": len(re.findall(r'\b\d+\b', prompt_text)),
            "action_verbs": len(re.findall(r'\b(create|generate|analyze|compare|list|describe|explain)\b', prompt_text.lower())),
            "measurable_criteria": len(re.findall(r'\b(exactly|precisely|at least|no more than|between)\b', prompt_text.lower())),
            "format_specifications": len(re.findall(r'\b(format|structure|style|template|json|csv)\b', prompt_text.lower())),
            "domain_specific_terms": random.randint(0, 10)  # Simulated domain terms
        }
        
        # Calculate specificity score
        specificity_score = 0
        specificity_score += specificity_analysis["specific_nouns"] * 5
        specificity_score += specificity_analysis["numbers_and_quantities"] * 10
        specificity_score += specificity_analysis["action_verbs"] * 8
        specificity_score += specificity_analysis["measurable_criteria"] * 15
        specificity_score += specificity_analysis["format_specifications"] * 12
        specificity_score += specificity_analysis["domain_specific_terms"] * 3
        
        specificity_analysis["specificity_score"] = min(100, specificity_score)
        
        return specificity_analysis
    
    def _analyze_prompt_context(self, prompt_text: str) -> Dict[str, Any]:
        """Analyze the contextual information provided in the prompt"""
        context_analysis = {
            "background_information": bool(re.search(r'\b(background|context|situation|scenario)\b', prompt_text.lower())),
            "role_definition": bool(re.search(r'\b(you are|act as|role|perspective)\b', prompt_text.lower())),
            "audience_specification": bool(re.search(r'\b(audience|reader|user|customer)\b', prompt_text.lower())),
            "purpose_statement": bool(re.search(r'\b(purpose|goal|objective|aim)\b', prompt_text.lower())),
            "domain_context": bool(re.search(r'\b(business|technical|medical|legal|educational)\b', prompt_text.lower())),
            "temporal_context": bool(re.search(r'\b(today|current|recent|historical|future)\b', prompt_text.lower())),
            "environmental_context": len(re.findall(r'\b(environment|setting|platform|system)\b', prompt_text.lower()))
        }
        
        # Calculate context score
        context_score = 0
        for key, value in context_analysis.items():
            if key != "environmental_context":
                if value:
                    context_score += 15
            else:
                context_score += value * 5
        
        context_analysis["context_score"] = min(100, context_score)
        
        return context_analysis
    
    def _apply_optimization_strategy(self, prompt_text: str, strategy: str, prompt_type: str) -> str:
        """Apply a specific optimization strategy to a prompt"""
        optimized_prompt = prompt_text
        
        if strategy == "clarity":
            # Improve clarity by simplifying language
            optimized_prompt = re.sub(r'\butilize\b', 'use', optimized_prompt, flags=re.IGNORECASE)
            optimized_prompt = re.sub(r'\bfacilitate\b', 'help', optimized_prompt, flags=re.IGNORECASE)
            optimized_prompt = re.sub(r'\bimplement\b', 'do', optimized_prompt, flags=re.IGNORECASE)
            
        elif strategy == "specificity":
            # Add more specific instructions
            if not re.search(r'\b(exactly|precisely|specifically)\b', optimized_prompt, re.IGNORECASE):
                optimized_prompt = "Please provide a detailed and specific " + optimized_prompt.lower()
            
        elif strategy == "context":
            # Add contextual information
            if not re.search(r'\b(context|background|situation)\b', optimized_prompt, re.IGNORECASE):
                context_addition = "Given the context of this request, "
                optimized_prompt = context_addition + optimized_prompt.lower()
            
        elif strategy == "examples":
            # Add example formatting
            if not re.search(r'\b(example|for instance)\b', optimized_prompt, re.IGNORECASE):
                optimized_prompt += "\n\nFor example, provide your response in a clear, structured format."
            
        elif strategy == "structure":
            # Improve structural organization
            if prompt_type == "instruction" and not re.search(r'\d+\.', optimized_prompt):
                lines = optimized_prompt.split('.')
                if len(lines) > 2:
                    structured_lines = [f"{i+1}. {line.strip()}" for i, line in enumerate(lines) if line.strip()]
                    optimized_prompt = '\n'.join(structured_lines)
            
        elif strategy == "constraints":
            # Add helpful constraints
            if not re.search(r'\b(should|must|avoid|don\'t)\b', optimized_prompt, re.IGNORECASE):
                optimized_prompt += " Please ensure your response is concise and relevant."
        
        return optimized_prompt
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        operation = input_data.get("operation", "status")
        
        if operation == "analyze_performance" and "analysis_config" in input_data:
            return self.analyze_prompt_performance(input_data["analysis_config"])
        elif operation == "optimize_prompts" and "optimization_config" in input_data:
            return self.optimize_prompts(input_data["optimization_config"])
        elif operation == "ab_test" and "ab_test_config" in input_data:
            return self.run_ab_tests(input_data["ab_test_config"])
        elif operation == "monitor_drift" and "monitoring_config" in input_data:
            return self.monitor_prompt_drift(input_data["monitoring_config"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["prompt_analysis", "optimization", "ab_testing", "drift_monitoring"],
            "optimization_strategies": self.optimization_strategies,
            "prompt_types": self.prompt_types,
            "evaluation_metrics": self.evaluation_metrics
        }

if __name__ == "__main__":
    agent = PromptTuner()
    print(json.dumps(agent.run(), indent=2))
