# BillingPlannerAI.py
import json
with open('../config/stripe_plans.json') as f:
    plans = json.load(f)['tiers']

def is_feature_unlocked(tier, feature):
    plan = next((p for p in plans if p['id'] == tier), None)
    return plan and feature in plan['features']

# Example: if is_feature_unlocked(user_tier, 'Video generation'):
# ...existing logic...
