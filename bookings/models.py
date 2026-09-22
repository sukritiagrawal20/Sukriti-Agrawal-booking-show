from django.conf import settings
from django.db import models

from shows.models import Seat, ShowTiming


class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    show_timing = models.ForeignKey(ShowTiming, on_delete=models.CASCADE, related_name="bookings")
    booking_id = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_id} - {self.user.username}"


class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booked_seats")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="booked_seats")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.booking.booking_id} - {self.seat.seat_number}"


class Coupon(models.Model):
    COUPON_TYPES = [("percent", "Percent"), ("flat", "Flat")]
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=COUPON_TYPES)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiry_date = models.DateField()
    usage_limit = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
