#!/usr/bin/env python3
"""
🎛️ Agent Manager - Central control hub for all Voyager agents
Manages agent states, provides CLI controls, and handles coordination
"""

import os
import yaml
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

class AgentManager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.agents_config_file = self.project_path / "app" / "assistant" / "agents" / "agents.yml"
        self.agents_config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # All available agents
        self.available_agents = [
            "PromptVoyager",
            "ShellVoyager",
            "SchemaVoyager",
            "UXVoyager",
            "ClaudeVoyager",
            "FeedbackVoyager",
            "PatchVoyager",
            "DeployVoyager",
            "CodeVoyager",
            "SecurityVoyager",
            "PerformanceVoyager",
            "ComplianceVoyager",
            "DataVoyager",
            "OptimizerVoyager",
            "OverseerVoyager",
            "ScoutVoyager",
            # New agents
            "DocVoyager",
            "TestVoyager",
            "InfraVoyager",
            "AlertVoyager",
            "LegalVoyager",
            "DataPrivacyVoyager",
            "DependencyVoyager",
            "LocalizationVoyager",
            "AIVoyager",
            # Advanced agents
            "ModelVoyager",
            "CustomerVoyager",
            "BackendVoyager",
            "PatentVoyager",
            "PatentResearchVoyager",
            "ClaimOptimizerVoyager",
            "DiagramVoyager",
            "RedFlagVoyager"
        ]
        
        # Initialize config if it doesn't exist
        if not self.agents_config_file.exists():
            self._create_default_config()
            
    def _create_default_config(self):
        """Create default agents.yml with all agents enabled"""
        default_config = {}
        
        for agent in self.available_agents:
            default_config[agent] = {
                "enabled": True,
                "priority": "normal",
                "timeout": 300,  # 5 minutes default timeout
                "retry_count": 1,
                "description": self._get_agent_description(agent)
            }
            
        with open(self.agents_config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
            
        print(f"✅ Created default agents config: {self.agents_config_file}")
        
    def _get_agent_description(self, agent_name):
        """Get description for each agent"""
        descriptions = {
            "PromptVoyager": "Auto-generates smart .prompt files from codebase analysis",
            "ShellVoyager": "Creates UI shells (SwiftUI/React/HTML) with routing",
            "SchemaVoyager": "Generates Pydantic/SQL/JSON schemas from data patterns",
            "UXVoyager": "Simulates user flows and detects UX issues",
            "ClaudeVoyager": "Strategic analysis and flow planning coordination",
            "FeedbackVoyager": "User interaction metrics and ML training data",
            "PatchVoyager": "Automated fix application from test failures",
            "DeployVoyager": "Deployment to TestFlight/App Store/staging",
            "CodeVoyager": "Deep code analysis, documentation, and refactoring",
            "SecurityVoyager": "Security scanning and vulnerability detection",
            "PerformanceVoyager": "Performance monitoring and optimization",
            "ComplianceVoyager": "License auditing and compliance verification",
            "DataVoyager": "Dataset drift and ETL pipeline health monitoring",
            "OptimizerVoyager": "AI model and prompt optimization",
            "OverseerVoyager": "Monitors and maintains other Voyager agents",
            "ScoutVoyager": "Computer vision and OCR capabilities",
            # New agents
            "DocVoyager": "Auto-generates and updates documentation (API, usage, diagrams)",
            "TestVoyager": "Generates, mutates, and analyzes test coverage",
            "InfraVoyager": "Detects IaC drift, cloud misconfig, automates setup",
            "AlertVoyager": "Routes all agent events to Slack/email",
            "LegalVoyager": "Detects license, copyright, export law issues",
            "DataPrivacyVoyager": "Scans for PII/PHI, flags risky data handling",
            "DependencyVoyager": "Audits, updates, and flags outdated/deprecated packages",
            "LocalizationVoyager": "Detects i18n/l10n gaps, updates translation files",
            "AIVoyager": "Monitors, retrains, and deploys ML models, manages drift"
        }
        return descriptions.get(agent_name, "Voyager agent")
        
    def load_config(self):
        """Load agents configuration"""
        try:
            with open(self.agents_config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
            
    def save_config(self, config):
        """Save agents configuration"""
        try:
            with open(self.agents_config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
            
    def is_agent_enabled(self, agent_name):
        """Check if specific agent is enabled"""
        config = self.load_config()
        agent_config = config.get(agent_name, {})
        return agent_config.get("enabled", False)
        
    def enable_agent(self, agent_name):
        """Enable specific agent"""
        config = self.load_config()
        if agent_name in config:
            config[agent_name]["enabled"] = True
            if self.save_config(config):
                print(f"✅ Enabled {agent_name}")
                return True
        else:
            print(f"❌ Unknown agent: {agent_name}")
        return False
        
    def disable_agent(self, agent_name):
        """Disable specific agent"""
        config = self.load_config()
        if agent_name in config:
            config[agent_name]["enabled"] = False
            if self.save_config(config):
                print(f"🔴 Disabled {agent_name}")
                return True
        else:
            print(f"❌ Unknown agent: {agent_name}")
        return False
        
    def enable_all(self):
        """Enable all agents"""
        config = self.load_config()
        for agent in config:
            config[agent]["enabled"] = True
            
        if self.save_config(config):
            print("✅ All agents enabled!")
            return True
        return False
        
    def disable_all(self):
        """Disable all agents"""
        config = self.load_config()
        for agent in config:
            config[agent]["enabled"] = False
            
        if self.save_config(config):
            print("🔴 All agents disabled!")
            return True
        return False
        
    def interactive_mode(self):
        """Interactive mode for enabling/disabling agents"""
        print("🎛️ Interactive Agent Manager")
        print("=" * 40)
        
        config = self.load_config()
        changes_made = False
        
        for agent in self.available_agents:
            if agent in config:
                current_status = "ENABLED" if config[agent]["enabled"] else "DISABLED"
                description = config[agent].get("description", "")
                
                print(f"\n{agent} - {description}")
                print(f"Current status: {current_status}")
                
                response = input(f"Enable {agent}? (Y/n/skip): ").strip().lower()
                
                if response in ['y', 'yes', '']:
                    config[agent]["enabled"] = True
                    changes_made = True
                    print(f"✅ {agent} enabled")
                elif response in ['n', 'no']:
                    config[agent]["enabled"] = False
                    changes_made = True
                    print(f"🔴 {agent} disabled")
                else:
                    print(f"⏭️  {agent} unchanged")
                    
        if changes_made and self.save_config(config):
            print("\n✅ Configuration saved!")
        else:
            print("\nℹ️  No changes made.")
            
    def show_status(self):
        """Show current status of all agents"""
        config = self.load_config()
        
        print("🎛️ Voyager Agent Fleet Status")
        print("=" * 50)
        
        enabled_count = 0
        disabled_count = 0
        
        for agent in self.available_agents:
            if agent in config:
                status = "🟢 ENABLED " if config[agent]["enabled"] else "🔴 DISABLED"
                description = config[agent].get("description", "")
                
                if config[agent]["enabled"]:
                    enabled_count += 1
                else:
                    disabled_count += 1
                    
                print(f"{status} {agent}")
                print(f"   {description}")
                print()
            else:
                print(f"⚠️  MISSING   {agent} (not in config)")
                print()
                
        print(f"📊 Summary: {enabled_count} enabled, {disabled_count} disabled")
        
    def export_env_vars(self):
        """Export agent states as environment variables"""
        config = self.load_config()
        
        for agent in self.available_agents:
            if agent in config:
                status = "true" if config[agent]["enabled"] else "false"
                env_var = f"AGENT_{agent.upper()}"
                print(f"{env_var}={status}")
                
    def check_agent(self, agent_name):
        """Check if agent is enabled (for Makefile integration)"""
        if self.is_agent_enabled(agent_name):
            return 0  # Enabled
        else:
            print(f"⏭️  {agent_name} is disabled - skipping")
            return 78  # Special exit code for "skip"
            
    def run_health_check(self):
        """Run health check on all enabled agents"""
        config = self.load_config()
        
        print("🔍 Running Voyager fleet health check...")
        
        health_results = {
            "timestamp": "2025-07-22T17:20:00Z",
            "total_agents": len(self.available_agents),
            "enabled_agents": 0,
            "healthy_agents": 0,
            "agent_status": {}
        }
        
        for agent in self.available_agents:
            if agent in config and config[agent]["enabled"]:
                health_results["enabled_agents"] += 1
                
                # Simple health check - verify agent file exists  
                agent_name = agent.replace("Voyager", "").lower() + "_voyager"
                agent_file = self.project_path / "app" / "assistant" / "agents" / f"{agent_name}.py"
                
                if agent_file.exists():
                    health_results["healthy_agents"] += 1
                    health_results["agent_status"][agent] = "healthy"
                    print(f"✅ {agent} - healthy")
                else:
                    health_results["agent_status"][agent] = "missing_file"
                    print(f"❌ {agent} - missing file")
            else:
                health_results["agent_status"][agent] = "disabled"
                print(f"⏭️  {agent} - disabled")
                
        print(f"\n📊 Health Summary: {health_results['healthy_agents']}/{health_results['enabled_agents']} enabled agents healthy")
        
        return health_results

def is_agent_enabled(agent_name):
    """Utility function for agents to check if they're enabled"""
    manager = AgentManager()
    return manager.is_agent_enabled(agent_name)

def main():
    parser = argparse.ArgumentParser(description="Voyager Agent Manager")
    parser.add_argument("--all-on", action="store_true", help="Enable all agents")
    parser.add_argument("--all-off", action="store_true", help="Disable all agents")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--status", action="store_true", help="Show agent status")
    parser.add_argument("--enable", nargs="+", help="Enable specific agents")
    parser.add_argument("--disable", nargs="+", help="Disable specific agents")
    parser.add_argument("--check", help="Check if specific agent is enabled")
    parser.add_argument("--export-env", action="store_true", help="Export environment variables")
    parser.add_argument("--health-check", action="store_true", help="Run health check")
    
    args = parser.parse_args()
    
    manager = AgentManager()
    
    if args.all_on:
        manager.enable_all()
    elif args.all_off:
        manager.disable_all()
    elif args.interactive:
        manager.interactive_mode()
    elif args.status:
        manager.show_status()
    elif args.enable:
        for agent in args.enable:
            manager.enable_agent(agent)
    elif args.disable:
        for agent in args.disable:
            manager.disable_agent(agent)
    elif args.check:
        return manager.check_agent(args.check)
    elif args.export_env:
        manager.export_env_vars()
    elif args.health_check:
        health_results = manager.run_health_check()
        print(json.dumps(health_results, indent=2))
    else:
        manager.show_status()
        
    return 0

if __name__ == "__main__":
    exit(main())
