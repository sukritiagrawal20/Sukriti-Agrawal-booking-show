from django import forms

from .models import Show, ShowTiming, Venue


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            "title",
            "description",
            "category",
            "genre",
            "language",
            "duration",
            "rating",
            "poster",
            "banner",
        ]


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ["name", "address", "city", "capacity", "seat_layout"]


class ShowTimingForm(forms.ModelForm):
    class Meta:
        model = ShowTiming
        fields = ["show", "venue", "date", "start_time", "end_time"]
