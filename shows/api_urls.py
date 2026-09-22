from django.urls import path

from . import views

urlpatterns = [
    path("shows/", views.api_show_list, name="api_show_list"),
    path("shows/<int:pk>/", views.api_show_detail, name="api_show_detail"),
    path("venues/", views.api_venue_list, name="api_venue_list"),
    path("showtimes/", views.api_showtime_list, name="api_showtime_list"),
    path("seats/<int:show_timing_id>/", views.api_seats_for_show_timing, name="api_seats"),
    path("coupons/validate/", views.validate_coupon_api, name="api_validate_coupon"),
]
