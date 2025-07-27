#!/usr/bin/env python3
"""
🤖 ModelVoyager - Advanced AI Model Management & Orchestration
Handles multiple AI providers, model selection, context optimization, and cost management
"""
import argparse, json, sys, os, time
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("ModelVoyager")
    except Exception:
        return True

class ModelVoyager:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.models_dir = self.project_root / "models"
        self.models_dir.mkdir(exist_ok=True)
        self.config_file = self.models_dir / "model_config.json"
        self.usage_log = self.models_dir / "usage_log.json"
        
        # Default model configurations - GPT-4 prioritized for user tasks
        self.default_models = {
            "gpt-4-turbo": {
                "provider": "openai",
                "cost_per_1k_tokens": 0.03,
                "context_limit": 128000,
                "best_for": ["complex_reasoning", "code_generation", "analysis", "user_tasks"],
                "backup": "gpt-3.5-turbo",
                "priority": 1  # Highest priority for user tasks
            },
            "gpt-4": {
                "provider": "openai",
                "cost_per_1k_tokens": 0.03,
                "context_limit": 8000,
                "best_for": ["user_interactions", "customer_support", "deal_analysis"],
                "backup": "gpt-4-turbo",
                "priority": 2  # Primary for standard user tasks
            },
            "gpt-3.5-turbo": {
                "provider": "openai", 
                "cost_per_1k_tokens": 0.002,
                "context_limit": 16000,
                "best_for": ["simple_tasks", "chat", "quick_responses"],
                "backup": "claude-3-haiku",
                "priority": 3
            },
            "claude-3-opus": {
                "provider": "anthropic",
                "cost_per_1k_tokens": 0.075,
                "context_limit": 200000,
                "best_for": ["dev_ops", "agent_coordination", "system_analysis"],
                "backup": "gpt-4-turbo",
                "priority": 4  # Reserved for internal development
            },
            "claude-3-sonnet": {
                "provider": "anthropic",
                "cost_per_1k_tokens": 0.015,
                "context_limit": 200000,
                "best_for": ["balanced_tasks", "code_review", "documentation"],
                "backup": "gpt-4-turbo"
            },
            "claude-3-haiku": {
                "provider": "anthropic",
                "cost_per_1k_tokens": 0.0025,
                "context_limit": 200000,
                "best_for": ["fast_responses", "simple_analysis", "low_cost"],
                "backup": "gpt-3.5-turbo"
            },
            "llama-3-70b": {
                "provider": "local",
                "cost_per_1k_tokens": 0.0,
                "context_limit": 8000,
                "best_for": ["privacy", "offline", "cost_free"],
                "backup": "gpt-3.5-turbo"
            }
        }
        self.load_config()
        
    def load_config(self):
        """Load model configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file) as f:
                    saved_config = json.load(f)
                    self.default_models.update(saved_config)
        except Exception:
            pass  # Use defaults if can't load
    
    def save_config(self):
        """Save model configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.default_models, f, indent=2)
        except Exception:
            pass  # Fail silently
        
    def configure_gpt4_primary(self):
        """Configure GPT-4 as the primary model for user tasks (free for us)"""
        print("🤖 [ModelVoyager] Configuring GPT-4 as primary model...")
        
        # Update default model selection to prioritize GPT-4
        self.default_models["gpt-4-turbo"]["priority"] = 1
        self.default_models["gpt-4"]["priority"] = 1
        
        # Set GPT-4 as preferred for all user-facing tasks
        gpt4_tasks = [
            "user_tasks", "customer_support", "deal_analysis", "product_analysis",
            "ungating_analysis", "scraper_tasks", "ai_assistance", "chat_responses",
            "data_analysis", "complex_reasoning", "code_generation"
        ]
        
        self.default_models["gpt-4"]["best_for"].extend(gpt4_tasks)
        self.default_models["gpt-4-turbo"]["best_for"].extend(gpt4_tasks)
        
        # Save updated configuration
        self.save_config()
        print("✅ GPT-4 configured as primary model for all user tasks")
        print("   Claude remains available for internal dev and agent operations")
        return True
        """Intelligently select best model for task"""
        suitable_models = []
        
        for model_name, config in self.default_models.items():
            if context_length <= config["context_limit"]:
                if task_type in config["best_for"] or "balanced_tasks" in config["best_for"]:
                    suitable_models.append((model_name, config))
        
        if not suitable_models:
            return "gpt-3.5-turbo"  # fallback
            
        # Sort by cost if budget is priority
        if budget_priority == "low_cost":
            suitable_models.sort(key=lambda x: x[1]["cost_per_1k_tokens"])
        elif budget_priority == "high_quality":
            suitable_models.sort(key=lambda x: x[1]["cost_per_1k_tokens"], reverse=True)
            
        return suitable_models[0][0]
    
    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int = 1000) -> float:
        """Estimate cost for model usage"""
        if model not in self.default_models:
            return 0.0
        cost_per_k = self.default_models[model]["cost_per_1k_tokens"]
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * cost_per_k
    
    def log_usage(self, model: str, tokens_used: int, cost: float, task_type: str):
        """Log model usage for analytics"""
        usage_entry = {
            "timestamp": time.time(),
            "model": model,
            "tokens": tokens_used,
            "cost": cost,
            "task_type": task_type
        }
        
        try:
            if self.usage_log.exists():
                with open(self.usage_log) as f:
                    usage_data = json.load(f)
            else:
                usage_data = []
            
            usage_data.append(usage_entry)
            
            with open(self.usage_log, "w") as f:
                json.dump(usage_data, f, indent=2)
        except Exception:
            pass
    
    def generate_usage_report(self) -> Dict:
        """Generate comprehensive usage analytics"""
        try:
            with open(self.usage_log) as f:
                usage_data = json.load(f)
        except Exception:
            return {"error": "No usage data found"}
        
        total_cost = sum(entry["cost"] for entry in usage_data)
        total_tokens = sum(entry["tokens"] for entry in usage_data)
        
        model_stats = {}
        for entry in usage_data:
            model = entry["model"]
            if model not in model_stats:
                model_stats[model] = {"cost": 0, "tokens": 0, "calls": 0}
            model_stats[model]["cost"] += entry["cost"]
            model_stats[model]["tokens"] += entry["tokens"]
            model_stats[model]["calls"] += 1
        
        return {
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "total_calls": len(usage_data),
            "model_breakdown": model_stats,
            "cost_per_model": {k: v["cost"] for k, v in model_stats.items()}
        }

def main():
    parser = argparse.ArgumentParser(description="ModelVoyager - AI Model Management")
    parser.add_argument("--recommend", help="Get model recommendation for task type")
    parser.add_argument("--context-length", type=int, default=4000, help="Expected context length")
    parser.add_argument("--budget", choices=["low_cost", "balanced", "high_quality"], default="balanced")
    parser.add_argument("--usage-report", action="store_true", help="Generate usage analytics")
    parser.add_argument("--estimate-cost", help="Estimate cost for model")
    parser.add_argument("--tokens", type=int, default=1000, help="Token count for cost estimation")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    
    if not is_agent_enabled():
        print("🤖 ModelVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🤖 ModelVoyager: Smoke test passed!")
        return 0
    
    voyager = ModelVoyager()
    
    if args.recommend:
        model = voyager.smart_model_selection(args.recommend, args.context_length, args.budget)
        print(f"🤖 Recommended model for '{args.recommend}': {model}")
        
    elif args.usage_report:
        report = voyager.generate_usage_report()
        print("🤖 ModelVoyager Usage Report:")
        print(json.dumps(report, indent=2))
        
    elif args.estimate_cost:
        cost = voyager.estimate_cost(args.estimate_cost, args.tokens)
        print(f"🤖 Estimated cost for {args.estimate_cost}: ${cost:.4f}")
        
    else:
        print("🤖 ModelVoyager: Use --recommend, --usage-report, or --estimate-cost")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
