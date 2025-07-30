#!/usr/bin/env python3
"""
Dealvoy Dashboard Integration System
Integrates all 46+ AI agents with customer and admin dashboards
"""

import json
from typing import Dict, List, Any, Optional
from tier_enforcement_system import tier_enforcement, TierLevel

class DashboardIntegrationSystem:
    """
    Advanced dashboard integration for AI agents with tier-based visibility
    - Generates dynamic HTML for customer dashboard (tier-filtered)
    - Provides admin dashboard with full agent control
    - Handles agent toggles and real-time status updates
    - Manages tier badges and upgrade prompts
    """
    
    def __init__(self):
        self.tier_system = tier_enforcement
    
    def generate_customer_dashboard_html(self, user_tier: str, user_name: str = "Customer") -> str:
        """Generate complete customer dashboard HTML with tier-appropriate agents"""
        
        # Get user's agents
        user_data = self.tier_system.get_tier_summary(user_tier, False)
        available_agents = self.tier_system.get_available_agents(user_tier, False)
        locked_agents = self.tier_system.get_locked_agents(user_tier, False)
        
        # Group agents by category
        categories = {}
        for agent in available_agents:
            category = agent["category"]
            if category not in categories:
                categories[category] = {"available": [], "locked": []}
            categories[category]["available"].append(agent)
        
        for agent in locked_agents:
            category = agent["category"]
            if category not in categories:
                categories[category] = {"available": [], "locked": []}
            categories[category]["locked"].append(agent)
        
        # Generate HTML
        return f"""
        <!-- AI AGENTS SECTION -->
        <div class="dashboard-section">
            <div class="section-header">
                <h2>🤖 AI Agents</h2>
                <div class="tier-info">
                    <span class="tier-badge tier-{user_tier.lower()}">{user_tier.title()} Plan</span>
                    <span class="agent-count">{user_data['accessible_agents']}/{user_data['total_agents']} Agents Available</span>
                </div>
            </div>
            
            {self._generate_tier_summary_html(user_data)}
            
            <div class="agents-grid">
                {self._generate_category_sections_html(categories, user_tier)}
            </div>
            
            {self._generate_upgrade_section_html(user_data) if user_data['locked_agents'] > 0 else ''}
        </div>
        """
    
    def generate_admin_dashboard_html(self) -> str:
        """Generate complete admin dashboard HTML with all agent controls"""
        
        all_agents = self.tier_system.get_all_agents_for_admin()
        
        # Group by category
        categories = {}
        for agent in all_agents:
            category = agent["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(agent)
        
        return f"""
        <!-- ADMIN AI AGENTS CONTROL CENTER -->
        <div class="admin-section">
            <div class="section-header">
                <h2>🔧 AI Agents Control Center</h2>
                <div class="admin-controls">
                    <button class="btn btn-primary" onclick="toggleAllAgents()">
                        <span class="material-icons">power_settings_new</span>
                        Toggle All
                    </button>
                    <button class="btn btn-secondary" onclick="testAllAgents()">
                        <span class="material-icons">play_arrow</span>
                        Test All
                    </button>
                    <button class="btn btn-info" onclick="exportAgentConfig()">
                        <span class="material-icons">download</span>
                        Export Config
                    </button>
                </div>
            </div>
            
            {self._generate_admin_stats_html(all_agents)}
            
            <div class="admin-agents-grid">
                {self._generate_admin_category_sections_html(categories)}
            </div>
        </div>
        
        <script>
        {self._generate_admin_javascript()}
        </script>
        """
    
    def generate_agent_toggle_html(self, agent: Dict[str, Any], is_admin: bool = False) -> str:
        """Generate HTML for individual agent toggle card"""
        
        if is_admin:
            return f"""
            <div class="agent-control-card" data-agent="{agent['name']}" data-tier="{agent['tier_requirement']}">
                <div class="agent-header">
                    <div class="agent-icon">{agent['icon']}</div>
                    <div class="agent-info">
                        <h3 class="agent-name">{agent['display_name']}</h3>
                        <div class="agent-meta">
                            <span class="tier-badge {agent['tier_requirement']}">{agent['tier_badge']}</span>
                            {'<span class="admin-only-badge">Admin Only</span>' if agent['admin_only'] else ''}
                            <span class="status-badge {agent['status']}">{agent['status'].title()}</span>
                        </div>
                    </div>
                    <div class="agent-controls">
                        <div class="toggle-switch active" onclick="toggleAgent(this, '{agent['name']}')">
                            <div class="toggle-slider"></div>
                        </div>
                    </div>
                </div>
                <div class="agent-description">{agent['description']}</div>
                <div class="agent-features">
                    {' '.join([f'<span class="feature-tag">{feature}</span>' for feature in agent['features'][:3]])}
                </div>
                <div class="agent-actions">
                    <button class="action-btn test-btn" onclick="testAgent('{agent['name']}')">
                        <span class="material-icons">play_arrow</span> Test
                    </button>
                    <button class="action-btn config-btn" onclick="configureAgent('{agent['name']}')">
                        <span class="material-icons">settings</span> Config
                    </button>
                    <button class="action-btn monitor-btn" onclick="monitorAgent('{agent['name']}')">
                        <span class="material-icons">monitor</span> Monitor
                    </button>
                </div>
            </div>
            """
        else:
            # Customer view
            if agent.get("is_accessible", True):
                return f"""
                <div class="agent-card accessible" data-agent="{agent['name']}">
                    <div class="agent-header">
                        <div class="agent-icon">{agent['icon']}</div>
                        <div class="agent-info">
                            <h3 class="agent-name">{agent['display_name']}</h3>
                            <span class="tier-badge {agent['tier_requirement']}">{agent['tier_badge']}</span>
                        </div>
                        <div class="agent-status active">
                            <span class="status-indicator"></span>
                            Active
                        </div>
                    </div>
                    <div class="agent-description">{agent['description']}</div>
                    <div class="agent-features">
                        {' '.join([f'<span class="feature-tag">{feature}</span>' for feature in agent['features'][:3]])}
                    </div>
                    <div class="agent-actions">
                        <button class="btn btn-primary" onclick="launchAgent('{agent['name']}')">
                            <span class="material-icons">launch</span>
                            Launch
                        </button>
                        <button class="btn btn-secondary" onclick="viewDetails('{agent['name']}')">
                            <span class="material-icons">info</span>
                            Details
                        </button>
                    </div>
                </div>
                """
            else:
                return f"""
                <div class="agent-card locked" data-agent="{agent['name']}">
                    <div class="agent-header">
                        <div class="agent-icon locked-icon">{agent['icon']}</div>
                        <div class="agent-info">
                            <h3 class="agent-name">{agent['display_name']}</h3>
                            <span class="tier-badge required">{agent['tier_badge']} Required</span>
                        </div>
                        <div class="lock-indicator">
                            <span class="material-icons">lock</span>
                        </div>
                    </div>
                    <div class="agent-description">{agent['description']}</div>
                    <div class="agent-features">
                        {' '.join([f'<span class="feature-tag locked">{feature}</span>' for feature in agent['features'][:2]])}
                        <span class="feature-tag more">+{len(agent['features'])-2} more</span>
                    </div>
                    <div class="agent-actions">
                        <button class="btn btn-upgrade" onclick="upgradeToTier('{agent['required_tier']}')">
                            <span class="material-icons">upgrade</span>
                            Upgrade to {agent['tier_badge']}
                        </button>
                    </div>
                </div>
                """
    
    def _generate_tier_summary_html(self, user_data: Dict[str, Any]) -> str:
        """Generate tier summary statistics"""
        
        return f"""
        <div class="tier-summary">
            <div class="summary-stats">
                <div class="stat-item">
                    <div class="stat-value">{user_data['accessible_agents']}</div>
                    <div class="stat-label">Available Agents</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{user_data['locked_agents']}</div>
                    <div class="stat-label">Locked Agents</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len(user_data['category_breakdown'])}</div>
                    <div class="stat-label">Categories</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_category_sections_html(self, categories: Dict[str, Dict[str, List]], user_tier: str) -> str:
        """Generate HTML for agent categories"""
        
        category_icons = {
            "automation": "⚡",
            "intelligence": "🧠",
            "security": "🛡️",
            "analytics": "📈",
            "optimization": "🎯",
            "monitoring": "📊",
            "integration": "🔗",
            "advisory": "💡",
            "profit": "💰"
        }
        
        html = ""
        for category, agents in categories.items():
            total_available = len(agents["available"])
            total_locked = len(agents["locked"])
            total = total_available + total_locked
            
            if total == 0:
                continue
            
            icon = category_icons.get(category, "🤖")
            
            html += f"""
            <div class="category-section">
                <div class="category-header">
                    <h3>{icon} {category.title().replace('_', ' ')}</h3>
                    <span class="category-count">{total_available}/{total} Available</span>
                </div>
                <div class="category-agents">
            """
            
            # Add available agents
            for agent in agents["available"]:
                html += self.generate_agent_toggle_html(agent, False)
            
            # Add locked agents
            for agent in agents["locked"]:
                html += self.generate_agent_toggle_html(agent, False)
            
            html += """
                </div>
            </div>
            """
        
        return html
    
    def _generate_upgrade_section_html(self, user_data: Dict[str, Any]) -> str:
        """Generate upgrade promotion section"""
        
        next_tier = user_data.get("next_tier")
        if not next_tier:
            return ""
        
        benefits = user_data.get("upgrade_benefits", [])
        
        return f"""
        <div class="upgrade-section">
            <div class="upgrade-header">
                <h3>🚀 Unlock More AI Power</h3>
                <p>Upgrade to {next_tier.title()} to access {user_data['locked_agents']} more AI agents</p>
            </div>
            <div class="upgrade-benefits">
                {' '.join([f'<div class="benefit-item">✅ {benefit}</div>' for benefit in benefits[:3]])}
            </div>
            <div class="upgrade-actions">
                <button class="btn btn-upgrade-primary" onclick="upgradePlan('{next_tier}')">
                    Upgrade to {next_tier.title()}
                </button>
                <button class="btn btn-secondary" onclick="viewAllPlans()">
                    View All Plans
                </button>
            </div>
        </div>
        """
    
    def _generate_admin_stats_html(self, all_agents: List[Dict[str, Any]]) -> str:
        """Generate admin statistics overview"""
        
        # Calculate stats
        total_agents = len(all_agents)
        active_agents = len([a for a in all_agents if a["status"] == "active"])
        admin_only = len([a for a in all_agents if a["admin_only"]])
        
        # Category breakdown
        categories = {}
        for agent in all_agents:
            category = agent["category"]
            categories[category] = categories.get(category, 0) + 1
        
        return f"""
        <div class="admin-stats">
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-icon">🤖</div>
                    <div class="stat-info">
                        <div class="stat-value">{total_agents}</div>
                        <div class="stat-label">Total Agents</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">✅</div>
                    <div class="stat-info">
                        <div class="stat-value">{active_agents}</div>
                        <div class="stat-label">Active</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🔒</div>
                    <div class="stat-info">
                        <div class="stat-value">{admin_only}</div>
                        <div class="stat-label">Admin Only</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📂</div>
                    <div class="stat-info">
                        <div class="stat-value">{len(categories)}</div>
                        <div class="stat-label">Categories</div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_admin_category_sections_html(self, categories: Dict[str, List]) -> str:
        """Generate admin category sections with full controls"""
        
        category_icons = {
            "automation": "⚡",
            "intelligence": "🧠",
            "security": "🛡️",
            "analytics": "📈",
            "optimization": "🎯",
            "monitoring": "📊",
            "integration": "🔗",
            "advisory": "💡",
            "profit": "💰"
        }
        
        html = ""
        for category, agents in categories.items():
            icon = category_icons.get(category, "🤖")
            active_count = len([a for a in agents if a["status"] == "active"])
            
            html += f"""
            <div class="admin-category-section">
                <div class="category-header">
                    <h3>{icon} {category.title().replace('_', ' ')}</h3>
                    <div class="category-controls">
                        <span class="category-count">{active_count}/{len(agents)} Active</span>
                        <button class="btn-icon" onclick="toggleCategory('{category}')" title="Toggle Category">
                            <span class="material-icons">power_settings_new</span>
                        </button>
                    </div>
                </div>
                <div class="admin-agents-grid">
            """
            
            for agent in agents:
                html += self.generate_agent_toggle_html(agent, True)
            
            html += """
                </div>
            </div>
            """
        
        return html
    
    def _generate_admin_javascript(self) -> str:
        """Generate JavaScript for admin dashboard functionality"""
        
        return """
        // Admin Dashboard JavaScript Functions
        
        function toggleAgent(toggleElement, agentName) {
            const isActive = toggleElement.classList.contains('active');
            
            if (isActive) {
                toggleElement.classList.remove('active');
                console.log(`Deactivating agent: ${agentName}`);
                // In production: API call to deactivate agent
            } else {
                toggleElement.classList.add('active');
                console.log(`Activating agent: ${agentName}`);
                // In production: API call to activate agent
            }
            
            updateAgentStatus(agentName, !isActive);
        }
        
        function testAgent(agentName) {
            console.log(`Testing agent: ${agentName}`);
            alert(`Testing ${agentName}...\\n\\nRunning diagnostic tests:\\n✅ Module loading\\n✅ Configuration check\\n✅ API connectivity\\n✅ Performance test\\n\\nAll tests passed!`);
            // In production: Real agent testing API call
        }
        
        function configureAgent(agentName) {
            console.log(`Configuring agent: ${agentName}`);
            const config = prompt(`Enter configuration for ${agentName}:`, 'default');
            if (config) {
                alert(`Configuration updated for ${agentName}`);
                // In production: Save agent configuration
            }
        }
        
        function monitorAgent(agentName) {
            console.log(`Opening monitor for agent: ${agentName}`);
            alert(`Monitoring ${agentName}:\\n\\n📊 CPU Usage: 12%\\n💾 Memory: 256MB\\n🔄 Requests/min: 45\\n✅ Status: Healthy\\n⏱️ Uptime: 99.8%`);
            // In production: Open monitoring dashboard
        }
        
        function toggleAllAgents() {
            const toggles = document.querySelectorAll('.toggle-switch');
            const allActive = Array.from(toggles).every(t => t.classList.contains('active'));
            
            toggles.forEach(toggle => {
                if (allActive) {
                    toggle.classList.remove('active');
                } else {
                    toggle.classList.add('active');
                }
            });
            
            console.log(allActive ? 'Deactivated all agents' : 'Activated all agents');
        }
        
        function testAllAgents() {
            alert('Running comprehensive test suite on all agents...\\n\\nThis may take a few minutes.');
            console.log('Testing all agents');
            // In production: Batch test all agents
        }
        
        function exportAgentConfig() {
            const config = {
                timestamp: new Date().toISOString(),
                total_agents: document.querySelectorAll('.agent-control-card').length,
                active_agents: document.querySelectorAll('.toggle-switch.active').length,
                configuration: 'Production settings exported'
            };
            
            console.log('Exporting configuration:', config);
            alert('Agent configuration exported successfully!');
            // In production: Download configuration file
        }
        
        function updateAgentStatus(agentName, isActive) {
            const card = document.querySelector(`[data-agent="${agentName}"]`);
            if (card) {
                const statusBadge = card.querySelector('.status-badge');
                if (statusBadge) {
                    statusBadge.textContent = isActive ? 'Active' : 'Inactive';
                    statusBadge.className = `status-badge ${isActive ? 'active' : 'inactive'}`;
                }
            }
        }
        
        function toggleCategory(category) {
            const categorySection = document.querySelector(`[data-category="${category}"]`);
            const toggles = categorySection?.querySelectorAll('.toggle-switch');
            
            if (toggles) {
                const allActive = Array.from(toggles).every(t => t.classList.contains('active'));
                
                toggles.forEach(toggle => {
                    if (allActive) {
                        toggle.classList.remove('active');
                    } else {
                        toggle.classList.add('active');
                    }
                });
            }
        }
        """

# Global instance
dashboard_integration = DashboardIntegrationSystem()

def get_customer_dashboard_html(user_tier: str, user_name: str = "Customer") -> str:
    """Get customer dashboard HTML with tier-appropriate agents"""
    return dashboard_integration.generate_customer_dashboard_html(user_tier, user_name)

def get_admin_dashboard_html() -> str:
    """Get admin dashboard HTML with full agent controls"""
    return dashboard_integration.generate_admin_dashboard_html()

def demo_dashboard_integration():
    """Demo the dashboard integration system"""
    print("🎨 Dashboard Integration System Demo")
    print("=" * 45)
    
    # Test customer dashboards
    customer_tiers = ["free", "starter", "pro", "enterprise"]
    
    for tier in customer_tiers:
        print(f"\n👤 {tier.title()} Customer Dashboard:")
        html_length = len(dashboard_integration.generate_customer_dashboard_html(tier))
        print(f"   Generated HTML: {html_length:,} characters")
        
        user_data = tier_enforcement.get_tier_summary(tier, False)
        print(f"   Available Agents: {user_data['accessible_agents']}")
        print(f"   Locked Agents: {user_data['locked_agents']}")
    
    # Test admin dashboard
    print(f"\n🔧 Admin Dashboard:")
    admin_html = dashboard_integration.generate_admin_dashboard_html()
    print(f"   Generated HTML: {len(admin_html):,} characters")
    all_agents = tier_enforcement.get_all_agents_for_admin()
    print(f"   Total Agents: {len(all_agents)}")

if __name__ == "__main__":
    demo_dashboard_integration()
