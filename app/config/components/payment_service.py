import os

import stripe

STRIPE = {
    'API_KEY': os.environ.get('STRIPE_API_KEY'),
    'WEBHOOK_KEY': os.environ.get('STRIPE_WEBHOOK_KEY'),
}

stripe.api_key = STRIPE['API_KEY']
