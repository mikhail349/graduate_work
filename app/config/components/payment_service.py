import os

import stripe

STRIPE = {
    'API_KEY': os.environ.get('STRIPE_API_KEY'),
    'WEBHOOK_KEY': os.environ.get('STRIPE_WEBHOOK_KEY'),
    'PORTAL_CONFIG_ID': os.environ.get('STRIPE_PORTAL_CONFIG_ID'),
}

stripe.api_key = STRIPE['API_KEY']
