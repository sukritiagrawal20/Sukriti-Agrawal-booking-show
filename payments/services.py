import hashlib
import hmac

from django.conf import settings


def create_razorpay_order(amount, receipt):
    return {
        "mock": True,
        "id": f"mock_order_{receipt}",
        "amount": int(float(amount) * 100),
        "currency": "INR",
        "receipt": receipt,
    }


def verify_razorpay_signature(order_id, payment_id, signature, secret):
    generated = hmac.new(
        secret.encode(),
        f"{order_id}|{payment_id}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(generated, signature)
