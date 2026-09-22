from django.urls import path

from . import views

urlpatterns = [
    path("", views.api_bookings, name="api_bookings"),
    path("<str:booking_id>/", views.api_booking_detail, name="api_booking_detail"),
    path("coupons/validate/", views.api_coupon_validate, name="api_coupon_validate"),
]
