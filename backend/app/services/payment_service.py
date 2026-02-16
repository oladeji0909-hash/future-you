import stripe
from app.core.config import settings
from app.models.user import SubscriptionTier
from typing import Dict, Optional
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

# Pricing configuration
PRICING = {
    SubscriptionTier.FREE: {
        "price": 0,
        "message_limit": 5,
        "features": ["5 messages per month", "Basic delivery timing", "Email notifications"]
    },
    SubscriptionTier.PREMIUM: {
        "price": 9.99,
        "stripe_price_id": "price_premium_monthly",  # Replace with actual Stripe price ID
        "message_limit": None,  # Unlimited
        "features": [
            "Unlimited messages",
            "AI-powered optimal timing",
            "Priority delivery",
            "Advanced analytics",
            "Custom companion personality",
            "Message reactions (video/audio)"
        ]
    },
    SubscriptionTier.LIFETIME: {
        "price": 99.00,
        "stripe_price_id": "price_lifetime_onetime",  # Replace with actual Stripe price ID
        "message_limit": None,  # Unlimited
        "features": [
            "Everything in Premium",
            "Lifetime access",
            "Early access to new features",
            "Priority support",
            "Blockchain verification",
            "Custom branding"
        ]
    }
}

class PaymentService:
    """Handle Stripe payments and subscription management"""
    
    @staticmethod
    def create_checkout_session(
        user_id: int,
        user_email: str,
        tier: SubscriptionTier,
        success_url: str,
        cancel_url: str
    ) -> Dict:
        """Create Stripe checkout session for subscription"""
        
        if tier == SubscriptionTier.FREE:
            return {"error": "Free tier doesn't require payment"}
        
        pricing = PRICING[tier]
        
        try:
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=["card"],
                line_items=[{
                    "price": pricing["stripe_price_id"],
                    "quantity": 1,
                }],
                mode="subscription" if tier == SubscriptionTier.PREMIUM else "payment",
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
                metadata={
                    "user_id": user_id,
                    "tier": tier.value
                },
                subscription_data={
                    "metadata": {
                        "user_id": user_id,
                        "tier": tier.value
                    }
                } if tier == SubscriptionTier.PREMIUM else None
            )
            
            return {
                "session_id": session.id,
                "url": session.url
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def create_customer_portal_session(
        customer_id: str,
        return_url: str
    ) -> Dict:
        """Create Stripe customer portal session for managing subscription"""
        
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            return {
                "url": session.url
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def handle_webhook_event(payload: bytes, sig_header: str) -> Dict:
        """Handle Stripe webhook events"""
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return {"error": "Invalid payload"}
        except stripe.error.SignatureVerificationError:
            return {"error": "Invalid signature"}
        
        # Handle different event types
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            return PaymentService._handle_checkout_completed(session)
        
        elif event["type"] == "customer.subscription.updated":
            subscription = event["data"]["object"]
            return PaymentService._handle_subscription_updated(subscription)
        
        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            return PaymentService._handle_subscription_cancelled(subscription)
        
        elif event["type"] == "invoice.payment_failed":
            invoice = event["data"]["object"]
            return PaymentService._handle_payment_failed(invoice)
        
        return {"status": "unhandled_event"}
    
    @staticmethod
    def _handle_checkout_completed(session: Dict) -> Dict:
        """Handle successful checkout"""
        
        user_id = session["metadata"]["user_id"]
        tier = session["metadata"]["tier"]
        
        return {
            "action": "upgrade_user",
            "user_id": user_id,
            "tier": tier,
            "stripe_customer_id": session.get("customer"),
            "stripe_subscription_id": session.get("subscription")
        }
    
    @staticmethod
    def _handle_subscription_updated(subscription: Dict) -> Dict:
        """Handle subscription update"""
        
        user_id = subscription["metadata"]["user_id"]
        status = subscription["status"]
        
        return {
            "action": "update_subscription_status",
            "user_id": user_id,
            "status": status,
            "current_period_end": subscription["current_period_end"]
        }
    
    @staticmethod
    def _handle_subscription_cancelled(subscription: Dict) -> Dict:
        """Handle subscription cancellation"""
        
        user_id = subscription["metadata"]["user_id"]
        
        return {
            "action": "downgrade_user",
            "user_id": user_id,
            "tier": SubscriptionTier.FREE.value
        }
    
    @staticmethod
    def _handle_payment_failed(invoice: Dict) -> Dict:
        """Handle failed payment"""
        
        customer_id = invoice["customer"]
        
        return {
            "action": "notify_payment_failed",
            "customer_id": customer_id,
            "amount_due": invoice["amount_due"]
        }
    
    @staticmethod
    def check_message_limit(user, db) -> Dict:
        """Check if user can create more messages based on their tier"""
        
        tier = user.subscription_tier
        pricing = PRICING[tier]
        
        # Unlimited for premium/lifetime
        if pricing["message_limit"] is None:
            return {"allowed": True, "remaining": None}
        
        # Count messages created this month
        from app.models.message import Message
        from sqlalchemy import func, extract
        
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        message_count = db.query(func.count(Message.id)).filter(
            Message.user_id == user.id,
            extract('month', Message.created_at) == current_month,
            extract('year', Message.created_at) == current_year
        ).scalar()
        
        limit = pricing["message_limit"]
        remaining = limit - message_count
        
        return {
            "allowed": remaining > 0,
            "remaining": remaining,
            "limit": limit,
            "upgrade_required": remaining <= 0
        }
    
    @staticmethod
    def get_pricing_info() -> Dict:
        """Get all pricing tier information"""
        return {
            "free": {
                "name": "Free",
                "price": PRICING[SubscriptionTier.FREE]["price"],
                "message_limit": PRICING[SubscriptionTier.FREE]["message_limit"],
                "features": PRICING[SubscriptionTier.FREE]["features"]
            },
            "premium": {
                "name": "Premium",
                "price": PRICING[SubscriptionTier.PREMIUM]["price"],
                "message_limit": PRICING[SubscriptionTier.PREMIUM]["message_limit"],
                "features": PRICING[SubscriptionTier.PREMIUM]["features"]
            },
            "lifetime": {
                "name": "Lifetime",
                "price": PRICING[SubscriptionTier.LIFETIME]["price"],
                "message_limit": PRICING[SubscriptionTier.LIFETIME]["message_limit"],
                "features": PRICING[SubscriptionTier.LIFETIME]["features"]
            }
        }
    
    @staticmethod
    def calculate_mrr(db) -> Dict:
        """Calculate Monthly Recurring Revenue"""
        
        from app.models.user import User
        from sqlalchemy import func
        
        # Count active premium subscribers (all premium users for now)
        premium_count = db.query(func.count(User.id)).filter(
            User.subscription_tier == SubscriptionTier.PREMIUM
        ).scalar() or 0
        
        # Lifetime is one-time, but we can amortize over 12 months for MRR calculation
        lifetime_count = db.query(func.count(User.id)).filter(
            User.subscription_tier == SubscriptionTier.LIFETIME
        ).scalar() or 0
        
        premium_mrr = premium_count * PRICING[SubscriptionTier.PREMIUM]["price"]
        lifetime_mrr = lifetime_count * (PRICING[SubscriptionTier.LIFETIME]["price"] / 12)
        
        total_mrr = premium_mrr + lifetime_mrr
        
        return {
            "total_mrr": round(total_mrr, 2),
            "premium_subscribers": premium_count,
            "lifetime_subscribers": lifetime_count,
            "total_subscribers": premium_count + lifetime_count,
            "goal": 10000,
            "progress_percentage": round((total_mrr / 10000) * 100, 2)
        }
