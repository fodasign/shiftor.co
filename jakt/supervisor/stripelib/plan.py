# coding=utf-8
import logging, stripe, json
logger = logging.getLogger(__name__)

# Django imports
from django.conf import settings

# Project imports
from utility.db.redis import get_connection as red_conn

# Internal imports
from .decorators import stripe_call
from . import customer

stripe.api_key = settings.STRIPE_SECRET

@stripe_call
def find (name):
    logger.debug("Looking for {0}".format(name))
    return stripe.Plan.retrieve(name)

@stripe_call
def available_plans (force=False, **kwargs):
    db = red_conn()
    plans = db.get("stripe:plans")
    if not plans or force:
        stripe_plans = stripe.Plan.all(**kwargs)
        plans = json.dumps([ ( p.get("id"), p.get("name") ) for p in stripe_plans.get("data") ])
        db.set("stripe:plans", plans)
    return json.loads(plans)

@stripe_call
def ensure_exists (plan):
    if not find(plan.name):
        logger.debug("Creating new plan {0}".format(plan.name))
        stripe.Plan.create(amount=plan.cents,
            id=plan.name,
            currency=plan.currency,
            interval=plan.interval,
            name="CC: Parcel Plan {0}".format(plan.name))

@stripe_call
def register_to_plan (payment, plan, **kwargs):
    ensure_exists(plan)
    customer_obj = customer.find(payment)
    if customer_obj.subscription:
        logger.error("Unable to overwrite an existing subscription.")
        return None
    customer_obj.update_subscription(plan=plan.name, prorate="False", **kwargs)

@stripe_call
def find_coupon (coupon_id):
    return stripe.Coupon.retrieve(coupon_id)

@stripe_call
def add_coupon (coupon):
    data = {
        "id" : coupon.unique_id,
        "currency" : "usd",
        "duration" : "forever",
        "max_redemptions" : coupon.uses
    }
    if coupon.cents:
        data["amount_off"] = coupon.cents
    else:
        data["percent_off"] = coupon.percent
    return stripe.Coupon.create(**data)

@stripe_call
def delete_coupon (coupon):
    c = find_coupon(coupon.unique_id)
    if c:
        c.delete()