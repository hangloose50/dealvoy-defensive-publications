from fastapi import APIRouter, Request, HTTPException
import stripe
import os

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_API_KEY")

@router.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Handle events
    if event['type'] == 'checkout.session.completed':
        # Grant access to user
        pass
    elif event['type'] == 'invoice.paid':
        # Update subscription status
        pass
    elif event['type'] == 'customer.subscription.updated':
        # Adjust agent/scan limits
        pass
    # Add more event handling as needed

    return {"status": "success"}
