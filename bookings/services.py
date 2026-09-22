from datetime import date

from django.db.models import Q

from .models import Coupon


def generate_booking_id():
    import random

    return f"BK-{random.randint(100000, 999999)}"


def validate_coupon(code, order_amount):
    if not code:
        return {"valid": False, "message": "Coupon code required."}

    try:
        coupon = Coupon.objects.get(code=code.upper(), active=True)
    except Coupon.DoesNotExist:
        return {"valid": False, "message": "Invalid coupon code."}

    if coupon.expiry_date < date.today():
        return {"valid": False, "message": "Coupon has expired."}

    if order_amount < float(coupon.minimum_amount):
        return {"valid": False, "message": f"Minimum order amount is ₹{coupon.minimum_amount}."}

    if coupon.discount_type == "percent":
        discount = order_amount * float(coupon.discount_value) / 100
    else:
        discount = float(coupon.discount_value)

    return {
        "valid": True,
        "coupon": coupon.code,
        "discount": round(discount, 2),
        "message": "Coupon applied successfully.",
    }
