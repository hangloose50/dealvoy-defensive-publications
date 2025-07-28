// AdminDashboard.tsx
import React from 'react';
import agentRegistry from '../config/agent_registry.json';
import stripePlans from '../config/stripe_plans.json';

function isTierUnlocked(tier: string, feature: string) {
  const plan = stripePlans.tiers.find(t => t.id === tier);
  return plan && plan.features.includes(feature);
}

// Example usage in AgentManager toggles:
// <Toggle disabled={!isTierUnlocked(userTier, 'Dedicated agent')} />

const AdminDashboard = () => {
  // ...existing dashboard code...
  return (
    <div>
      <h2>Admin Dashboard</h2>
      {/* AgentManager toggles and tier enforcement logic here */}
    </div>
  );
};

export default AdminDashboard;
