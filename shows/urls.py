from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search_results, name="search_results"),
    path("show/<int:pk>/", views.show_detail, name="show_detail"),
    path("venue/<int:pk>/", views.venue_detail, name="venue_detail"),
    path("booking/select-seats/<int:show_timing_id>/", views.select_seats, name="select_seats"),
    path("booking/summary/<int:show_timing_id>/", views.booking_summary, name="booking_summary"),
    path("booking/confirmation/<str:booking_id>/", views.confirmation, name="confirmation"),
    path("booking/<str:booking_id>/qr/", views.ticket_qr, name="ticket_qr"),
    path("booking/<str:booking_id>/ticket.pdf", views.ticket_pdf, name="ticket_pdf"),
    path("bookings/my/", views.my_bookings, name="my_bookings"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("movies/", views.catalog, {"category": "movies"}, name="movies"),
    path("shows/", views.catalog, {"category": "shows"}, name="shows"),
    path("events/", views.catalog, {"category": "events"}, name="events"),
    path("sports/", views.catalog, {"category": "sports"}, name="sports"),
    path("concerts/", views.catalog, {"category": "concerts"}, name="concerts"),
    path("theatre/", views.catalog, {"category": "theatre"}, name="theatre"),
]