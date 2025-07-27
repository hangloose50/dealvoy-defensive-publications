# Patent/IP agents
patent-voyager:
	python3 app/assistant/agents/patent_voyager.py --type provisional

patent-research:
	python3 app/assistant/agents/patent_research_voyager.py --query "your-topic"
# Model snapshot and patent export
snapshot-model:
	python3 scripts/model_snapshot.py
	echo "Model snapshot saved to dist/"
# Dev cycle: test all agents and build bundle
dev-cycle:
	make all-voyagers
	make offline-bundle
# Offline bundle
offline-bundle:
	python3 scripts/offline_packager.py
	echo "Bundle created: dist/dealvoy_offline_bundle.zip"
# ScoutVision pipeline
scout-voyager:
	python3 app/assistant/agents/scout_voyager.py

claim-optimizer-voyager:
	python3 app/assistant/agents/claim_optimizer_voyager.py $(ARGS)

diagram-voyager:
	python3 app/assistant/agents/diagram_voyager.py $(ARGS)

red-flag-voyager:
	python3 app/assistant/agents/red_flag_voyager.py $(ARGS)

model-voyager:
	python3 app/assistant/agents/model_voyager.py $(ARGS)

customer-voyager:
	python3 app/assistant/agents/customer_voyager.py $(ARGS)

backend-voyager:
	python3 app/assistant/agents/backend_voyager.py $(ARGS)

dealscorer-voyager:
	python3 app/assistant/agents/dealscorer_voyager.py --input $(INPUT) $(ARGS)

ungating-voyager:
	python3 app/assistant/agents/ungating_voyager.py --input $(INPUT) $(ARGS)

scraper-infrastructure-voyager:
	python3 app/assistant/agents/scraper_infrastructure_voyager.py $(ARGS)

# SaaS Platform Deployment Agents
web-voyager:
	python3 app/assistant/agents/web_voyager.py $(ARGS)

brand-voyager:
	python3 app/assistant/agents/brand_voyager.py $(ARGS)

stripe-voyager:
	python3 app/assistant/agents/stripe_voyager.py $(ARGS)

admin-voyager:
	python3 app/assistant/agents/admin_voyager.py $(ARGS)
# AmazonScraperToolkit & Voyager Agent System Makefile
# Complete development workflow automation

.PHONY: help install test clean run-orchestrator voyager-help all-voyagers

# Default target
help:
	@echo "🚀 AmazonScraperToolkit & Voyager Agent System"
	@echo ""
	@echo "Core Commands:"
	@echo "  make install          Install dependencies"
	@echo "  make test             Run test suite"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make clean            Clean cache and temp files"
	@echo "  make run-orchestrator Start the main orchestrator"
	@echo ""
	@echo "🛸 Voyager Agent Commands:"
	@echo "  make prompt-voyager   Generate smart .prompt files from codebase"
	@echo "  make shell-voyager    Create SwiftUI/React/HTML app shells"
	@echo "  make schema-voyager   Generate Pydantic/SQL/JSON schemas"
	@echo "  make ux-voyager       Simulate user flows and detect UX issues"
	@echo "  make claude-voyager   Strategic analysis and flow planning"
	@echo "  make feedback-voyager Collect user interaction metrics"
	@echo "  make patch-voyager    Automated fix application from test failures"
	@echo "  make deploy-voyager   Deploy to TestFlight/App Store/staging"
	@echo "  make code-voyager     Analyze and improve codebase automatically"
	@echo ""
	@echo "🌟 Meta Commands:"
	@echo "  make all-voyagers     Run all Voyager agents in sequence"
	@echo "  make voyager-help     Detailed help for Voyager system"

# Installation
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Testing
test:
	@echo "🧪 Running test suite..."
	python -m pytest tests/ -v
	@echo "✅ Tests complete!"

test-watch:
	@echo "👀 Running tests in watch mode..."
	python -m pytest tests/ -v --tb=short -x --ff

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache/
	rm -rf dist/
	rm -rf *.egg-info/
	@echo "✅ Cleanup complete!"

# Main orchestrator
run-orchestrator:
	@echo "🎯 Starting orchestrator..."
	cd app && python orchestrator.py

# Individual agent targets
prompt-voyager:
	@python app/assistant/agents/prompt_voyager.py

shell-voyager:
	@python app/assistant/agents/shell_voyager.py

schema-voyager:
	@python app/assistant/agents/schema_voyager.py

ux-voyager:
	@python app/assistant/agents/ux_voyager.py

claude-voyager:
	@python app/assistant/agents/claude_voyager.py

feedback-voyager:
	@python app/assistant/agents/feedback_voyager.py

patch-voyager:
	@python app/assistant/agents/patch_voyager.py

deploy-voyager:
	@python app/assistant/agents/deploy_voyager.py

code-voyager:
	@python app/assistant/agents/code_voyager.py

security-voyager:
	@python app/assistant/agents/security_voyager.py

performance-voyager:
	@python app/assistant/agents/performance_voyager.py

compliance-voyager:
	@python app/assistant/agents/compliance_voyager.py

data-voyager:
	@python app/assistant/agents/data_voyager.py

optimizer-voyager:
	@python app/assistant/agents/optimizer_voyager.py

overseer-voyager:
	@python app/assistant/agents/overseer_voyager.py

# Meta targets
all-voyagers:
	@echo "🚀 Running all 15 Voyager agents..."
	@$(MAKE) prompt-voyager shell-voyager schema-voyager ux-voyager claude-voyager feedback-voyager patch-voyager deploy-voyager code-voyager security-voyager performance-voyager compliance-voyager data-voyager optimizer-voyager overseer-voyager

core-voyagers:
	@echo "🎯 Running core 9 Voyager agents..."
	@$(MAKE) prompt-voyager shell-voyager schema-voyager ux-voyager claude-voyager feedback-voyager patch-voyager deploy-voyager code-voyager

expansion-voyagers:
	@echo "⚡ Running expansion 6 Voyager agents..."
	@$(MAKE) security-voyager performance-voyager compliance-voyager data-voyager optimizer-voyager overseer-voyager

smoke-test-all:
	@echo "💨 Running smoke tests for all agents..."
	@python app/assistant/agents/prompt_voyager.py --smoke-test
	@python app/assistant/agents/shell_voyager.py --smoke-test
	@python app/assistant/agents/schema_voyager.py --smoke-test
	@python app/assistant/agents/ux_voyager.py --smoke-test
	@python app/assistant/agents/claude_voyager.py --smoke-test
	@python app/assistant/agents/feedback_voyager.py --smoke-test
	@python app/assistant/agents/patch_voyager.py --smoke-test
	@python app/assistant/agents/deploy_voyager.py --smoke-test
	@python app/assistant/agents/code_voyager.py --smoke-test
	@python app/assistant/agents/security_voyager.py --smoke-test
	@python app/assistant/agents/performance_voyager.py --smoke-test
	@python app/assistant/agents/compliance_voyager.py --smoke-test
	@python app/assistant/agents/data_voyager.py --smoke-test
	@python app/assistant/agents/optimizer_voyager.py --smoke-test
	@python app/assistant/agents/overseer_voyager.py --smoke-test

agent-health:
	@echo "� Checking agent health via OverseerVoyager..."
	@python app/assistant/agents/overseer_voyager.py

agent-manager:
	@echo "🎛️ Running Agent Manager..."
	@python app/assistant/agents/agent_manager.py --status

voyager-help:
	@echo "🛸 Voyager Agent System - Detailed Help"
	@echo ""
	@echo "The Voyager Agent System consists of 9 specialized agents:"
	@echo ""
	@echo "1. 🎯 PromptVoyager (prompt-voyager)"
	@echo "   • Auto-generates optimized .prompt files from codebase analysis"
	@echo "   • Detects patterns and creates context-aware templates"
	@echo "   • Improves AI interaction quality"
	@echo ""
	@echo "2. 🏗️  ShellVoyager (shell-voyager)"
	@echo "   • Creates SwiftUI/React/HTML app shells with routing"
	@echo "   • Detects frameworks and generates appropriate boilerplate"
	@echo "   • Accelerates UI development startup"
	@echo ""
	@echo "3. 📋 SchemaVoyager (schema-voyager)"
	@echo "   • Generates Pydantic/SQL/JSON schemas from data patterns"
	@echo "   • Analyzes existing data structures"
	@echo "   • Creates validation and migration scripts"
	@echo ""
	@echo "4. 👤 UXVoyager (ux-voyager)"
	@echo "   • Simulates user flows with screenshots and issue detection"
	@echo "   • Tests user journeys automatically"
	@echo "   • Identifies UX bottlenecks and improvements"
	@echo ""
	@echo "5. 🧠 ClaudeVoyager (claude-voyager)"
	@echo "   • Strategic analysis and flow planning coordination"
	@echo "   • High-level project direction and optimization"
	@echo "   • Cross-agent coordination and planning"
	@echo ""
	@echo "6. 📊 FeedbackVoyager (feedback-voyager)"
	@echo "   • User interaction metrics and ML training data collection"
	@echo "   • A/B testing coordination"
	@echo "   • Performance analytics and insights"
	@echo ""
	@echo "7. 🔧 PatchVoyager (patch-voyager)"
	@echo "   • Automated fix application from test failures"
	@echo "   • Pattern matching for error types"
	@echo "   • Continuous improvement and monitoring"
	@echo ""
	@echo "8. 🚀 DeployVoyager (deploy-voyager)"
	@echo "   • Deployment to TestFlight, App Store, and staging"
	@echo "   • Automated builds, tests, and health checks"
	@echo "   • Rollback capabilities and monitoring"
	@echo ""
	@echo "9. 💻 CodeVoyager (code-voyager)"
	@echo "   • Deep codebase analysis and structure mapping"
	@echo "   • Auto-documentation and API reference generation"
	@echo "   • Refactoring suggestions and code quality improvements"
	@echo "   • Integration with linting and formatting tools"
	@echo ""
	@echo "Usage Examples:"
	@echo "  make all-voyagers     # Run complete development cycle"
	@echo "  make prompt-voyager   # Generate prompts for current codebase"
	@echo "  make code-voyager     # Analyze code quality and generate docs"
	@echo "  make deploy-voyager   # Deploy to staging environment"
	@echo ""
	@echo "💡 Each agent generates detailed reports in their respective directories"

# Development workflow shortcuts
dev-cycle: clean test all-voyagers
	@echo "🎯 Complete development cycle finished!"

quick-test: test prompt-voyager patch-voyager
	@echo "🚀 Quick test and fix cycle complete!"

deploy-ready: test all-voyagers deploy-voyager
	@echo "🚀 Ready for deployment!"

# Scout Integration (Future Enhancement)
scout-vision:
	@echo "📸 [Future] ScoutVision + OCR integration coming soon..."
	@echo "   • Camera capture and Tesseract OCR processing"
	@echo "   • Real-time product detection and analysis"

# Project structure
show-structure:
	@echo "📁 Project Structure:"
	@tree -I '__pycache__|*.pyc|.git' -L 3

# Quick status check
status:
	@echo "📊 Project Status:"
	@echo "   Python Version: $(shell python --version)"
	@echo "   Pytest Status: $(shell python -m pytest tests/ --tb=no -q | tail -1)"
	@echo "   Agent Count: 8 Voyager Agents Available"
	@echo "   Core Status: Orchestrator Operational"
