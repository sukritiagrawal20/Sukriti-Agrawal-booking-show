from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)
    seat_layout = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Show(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[("Movie", "Movie"), ("Show", "Show"), ("Event", "Event")])
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="In minutes")
    rating = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)
    poster_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ShowTiming(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="show_timings")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="show_timings")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.show.title} - {self.venue.name} - {self.date}"

    def available_seats(self):
        seats = Seat.objects.filter(venue=self.venue).order_by("seat_number")
        return [seat for seat in seats if self.is_seat_available(seat)]

    def is_seat_available(self, seat):
        from bookings.models import BookedSeat

        return not BookedSeat.objects.filter(seat=seat, booking__show_timing=self, booking__booking_status__in=["Confirmed", "Pending"]).exists()


class Seat(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=[("Regular", "Regular"), ("Premium", "Premium"), ("VIP", "VIP")])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ("venue", "seat_number")

    def __str__(self):
        return f"{self.venue.name} - {self.seat_number}"
