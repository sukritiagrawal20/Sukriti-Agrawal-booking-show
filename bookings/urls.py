from django.urls import path

from . import views

urlpatterns = [
    path("create/<int:show_timing_id>/", views.create_booking, name="create_booking"),
    path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("detail/<str:booking_id>/", views.booking_detail, name="booking_detail"),
    path("cancel/<str:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("api/", views.api_bookings, name="api_bookings"),
    path("api/<str:booking_id>/", views.api_booking_detail, name="api_booking_detail"),
    path("api/coupons/validate/", views.api_coupon_validate, name="api_coupon_validate"),
]
