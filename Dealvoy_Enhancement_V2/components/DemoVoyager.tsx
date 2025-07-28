// DemoVoyager.tsx
import React from 'react';
import stripePlans from '../config/stripe_plans.json';

function canPreviewVideo(tier: string) {
  const plan = stripePlans.tiers.find(t => t.id === tier);
  return plan && plan.video;
}

// Example usage:
// {canPreviewVideo(userTier) && <VideoPreviewComponent />}

const DemoVoyager = ({ userTier }) => (
  <div>
    <h2>Demo Voyager</h2>
    {canPreviewVideo(userTier) ? <div>Video Preview Enabled</div> : <div>Upgrade to Titan+ for video preview</div>}
  </div>
);

export default DemoVoyager;
