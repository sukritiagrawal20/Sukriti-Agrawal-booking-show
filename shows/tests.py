from django.contrib.auth import get_user_model
from django.test import TestCase

from bookings.models import Booking, BookedSeat
from shows.models import Seat, Show, ShowTiming, Venue


class BookingFlowTests(TestCase):
    def test_show_timing_tracks_available_seats(self):
        venue = Venue.objects.create(
            name="PVR Jaipur",
            address="Malviya Nagar",
            city="Jaipur",
            capacity=10,
            seat_layout="A1-A5",
        )
        show = Show.objects.create(
            title="Avengers",
            description="A superhero movie.",
            category="Movie",
            genre="Action",
            language="Hindi",
            duration=150,
            rating=4.7,
            poster="poster.png",
            banner="banner.png",
        )
        show_timing = ShowTiming.objects.create(
            show=show,
            venue=venue,
            date="2026-09-25",
            start_time="10:00:00",
            end_time="12:30:00",
        )
        seat = Seat.objects.create(venue=venue, seat_number="A1", category="Regular", price=500)

        self.assertIn(seat, show_timing.available_seats())

    def test_booking_prevents_duplicate_seat_booking(self):
        user = get_user_model().objects.create_user(username="testuser", password="secret123")
        venue = Venue.objects.create(
            name="INOX Delhi",
            address="Saket",
            city="Delhi",
            capacity=10,
            seat_layout="A1-A5",
        )
        show = Show.objects.create(
            title="Dune",
            description="Sci-fi epic.",
            category="Movie",
            genre="Sci-Fi",
            language="English",
            duration=165,
            rating=4.8,
            poster="poster.png",
            banner="banner.png",
        )
        show_timing = ShowTiming.objects.create(
            show=show,
            venue=venue,
            date="2026-09-26",
            start_time="18:00:00",
            end_time="20:45:00",
        )
        seat = Seat.objects.create(venue=venue, seat_number="B2", category="Premium", price=750)
        booking = Booking.objects.create(
            user=user,
            show_timing=show_timing,
            booking_id="BK-1001",
            total_amount=750,
            discount=0,
            payment_id="pay_1",
            booking_status="Confirmed",
        )
        BookedSeat.objects.create(booking=booking, seat=seat, price=750)

        self.assertFalse(show_timing.is_seat_available(seat))
