from django.conf import settings
from django.db import models

from bookings.models import Booking


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=30, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.booking_id} - {self.status}"
