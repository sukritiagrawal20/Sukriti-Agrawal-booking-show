import json
from io import BytesIO
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking, BookedSeat
from bookings.services import generate_booking_id, validate_coupon
from payments.services import create_razorpay_order
from .forms import ShowForm, ShowTimingForm, VenueForm
from .models import Seat, Show, ShowTiming, Venue


def home(request):
    shows = Show.objects.all().order_by("-rating", "title")
    city = request.GET.get("city") or request.session.get("city", "Jaipur")
    if city:
        request.session["city"] = city
    city_shows = shows.filter(show_timings__venue__city__iexact=city).distinct()
    if not city_shows.exists():
        city_shows = shows
    context = {
        "shows": city_shows[:8],
        "movies": city_shows.filter(category="Movie")[:8],
        "events": city_shows.filter(category="Event")[:6],
        "venues": list(Venue.objects.filter(city__iexact=city)[:6]) or list(Venue.objects.all()[:6]),
        "city": city,
    }
    return render(request, "home.html", context)




def catalog(request, category="all"):
    city = request.GET.get("city") or request.session.get("city", "Jaipur")
    if city:
        request.session["city"] = city
    queryset = Show.objects.all().order_by("-rating", "title")
    if category == "movies":
        queryset = queryset.filter(category="Movie")
    elif category == "shows":
        queryset = queryset.filter(category="Show")
    elif category == "events":
        queryset = queryset.filter(category="Event")
    elif category in {"sports", "concerts", "theatre"}:
        queryset = queryset.filter(genre__icontains=category[:-1] if category == "sports" else category[:-1] if category == "concerts" else "drama")
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(genre__icontains=query))
    genre = request.GET.get("genre")
    language = request.GET.get("language")
    if genre:
        queryset = queryset.filter(genre__iexact=genre)
    if language:
        queryset = queryset.filter(language__iexact=language)
    sort = request.GET.get("sort")
    if sort == "rating":
        queryset = queryset.order_by("-rating")
    elif sort == "newest":
        queryset = queryset.order_by("-created_at")
    return render(request, "catalog.html", {"shows": queryset, "category": category, "city": city, "query": query})
def search_results(request):
    query = request.GET.get("q", "")
    city = request.GET.get("city")
    category = request.GET.get("category")
    genre = request.GET.get("genre")
    language = request.GET.get("language")
    sort = request.GET.get("sort", "-rating")

    queryset = Show.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(genre__icontains=query) |
        Q(category__icontains=query) |
        Q(language__icontains=query)
    )
    if city:
        queryset = queryset.filter(show_timings__venue__city__icontains=city).distinct()
    if category:
        queryset = queryset.filter(category__icontains=category)
    if genre:
        queryset = queryset.filter(genre__icontains=genre)
    if language:
        queryset = queryset.filter(language__icontains=language)

    try:
        queryset = queryset.order_by(sort)
    except Exception:
        queryset = queryset.order_by("-rating")

    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "search_results.html", {"page_obj": page_obj, "query": query})


def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    timings = show.show_timings.select_related("venue").order_by("date", "start_time")
    return render(request, "show_details.html", {"show": show, "timings": timings})


def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    timings = ShowTiming.objects.filter(venue=venue).select_related("show").order_by("date", "start_time")
    return render(request, "venue_detail.html", {"venue": venue, "timings": timings})


@login_required
def select_seats(request, show_timing_id):
    show_timing = get_object_or_404(ShowTiming, pk=show_timing_id)
    seats = Seat.objects.filter(venue=show_timing.venue).order_by("seat_number")
    booked_seats = set(
        BookedSeat.objects.filter(booking__show_timing=show_timing, booking__booking_status__in=["Confirmed", "Pending"]).values_list("seat__seat_number", flat=True)
    )
    booked_seat_list = sorted(booked_seats)
    return render(request, "seat_selection.html", {"show_timing": show_timing, "seats": seats, "booked_seats": json.dumps(booked_seat_list), "booked_seat_list": booked_seat_list})


@login_required
def booking_summary(request, show_timing_id):
    show_timing = get_object_or_404(ShowTiming, pk=show_timing_id)
    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")
        if not selected_seats:
            messages.error(request, "Please select at least one seat.")
            return redirect("select_seats", show_timing_id=show_timing.id)

        seat_objs = list(Seat.objects.filter(venue=show_timing.venue, seat_number__in=selected_seats))
        if len(seat_objs) != len(selected_seats):
            messages.error(request, "One or more seats are invalid.")
            return redirect("select_seats", show_timing_id=show_timing.id)

        booking_data = {
            "show_timing": show_timing,
            "selected_seats": selected_seats,
            "seat_objs": seat_objs,
            "base_amount": sum(float(seat.price) for seat in seat_objs),
            "convenience_fee": 30 * len(seat_objs),
            "tax": 20 * len(seat_objs),
        }
        request.session["booking_data"] = {
            "show_timing_id": show_timing.id,
            "selected_seats": selected_seats,
            "base_amount": str(booking_data["base_amount"]),
            "convenience_fee": str(booking_data["convenience_fee"]),
            "tax": str(booking_data["tax"]),
        }
        return render(request, "booking_summary.html", {"show_timing": show_timing, "seats": seat_objs, "booking_data": booking_data})

    return redirect("select_seats", show_timing_id=show_timing.id)


@login_required
def confirmation(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, "confirmation.html", {"booking": booking})


@login_required
def ticket_qr(request, booking_id):
    import qrcode

    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    image = qrcode.make(f"SHOWBOOK|{booking.booking_id}|{booking.show_timing.show.title}")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def ticket_pdf(request, booking_id):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{booking.booking_id}.pdf"'
    document = canvas.Canvas(response, pagesize=A4)
    document.setTitle(f"ShowBook Ticket {booking.booking_id}")
    document.setFont("Helvetica-Bold", 24)
    document.drawString(60, 780, "SHOWBOOK")
    document.setFont("Helvetica-Bold", 18)
    document.drawString(60, 735, booking.show_timing.show.title)
    document.setFont("Helvetica", 12)
    lines = [
        f"Booking ID: {booking.booking_id}",
        f"Venue: {booking.show_timing.venue.name}",
        f"Date: {booking.show_timing.date}",
        f"Time: {booking.show_timing.start_time}",
        f"Seats: {', '.join(item.seat.seat_number for item in booking.booked_seats.select_related('seat'))}",
        f"Amount paid: INR {booking.total_amount}",
        f"Status: {booking.booking_status}",
    ]
    y = 690
    for line in lines:
        document.drawString(60, y, line)
        y -= 28
    document.drawString(60, y - 10, "Present this ticket at the venue entrance.")
    document.showPage()
    document.save()
    return response


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_bookings.html", {"bookings": bookings})


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    users_count = 0
    total_shows = Show.objects.count()
    total_events = Show.objects.filter(category="Event").count()
    total_bookings = Booking.objects.count()
    bookings_today = Booking.objects.filter(created_at__date=datetime.today().date()).count()
    total_revenue = Booking.objects.filter(booking_status="Confirmed").aggregate(total=Sum("total_amount")) ["total"] or 0
    upcoming_shows = ShowTiming.objects.filter(date__gte=datetime.today().date()).count()

    daily_bookings = (
        Booking.objects.extra(select={"day": "date(created_at)"})
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    status_data = Booking.objects.values("booking_status").annotate(count=Count("id"))
    return render(
        request,
        "admin_dashboard.html",
        {
            "total_users": users_count,
            "total_shows": total_shows,
            "total_events": total_events,
            "total_bookings": total_bookings,
            "bookings_today": bookings_today,
            "total_revenue": total_revenue,
            "upcoming_shows": upcoming_shows,
            "daily_bookings": daily_bookings,
            "status_data": status_data,
        },
    )


# admin management helpers

def admin_manage_show(request):
    form = ShowForm()
    return render(request, "admin_show_form.html", {"form": form})


def admin_manage_venue(request):
    form = VenueForm()
    return render(request, "admin_venue_form.html", {"form": form})


def admin_manage_show_timing(request):
    form = ShowTimingForm()
    return render(request, "admin_show_timing_form.html", {"form": form})


def api_show_list(request):
    items = list(Show.objects.values("id", "title", "category", "genre", "language", "rating"))
    return JsonResponse({"results": items})


def api_show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    return JsonResponse({
        "id": show.id,
        "title": show.title,
        "description": show.description,
        "category": show.category,
        "genre": show.genre,
        "language": show.language,
        "rating": show.rating,
    })


def api_venue_list(request):
    items = list(Venue.objects.values("id", "name", "city", "address"))
    return JsonResponse({"results": items})


def api_showtime_list(request):
    items = list(ShowTiming.objects.select_related("show", "venue").values("id", "show__title", "venue__name", "date", "start_time", "end_time"))
    return JsonResponse({"results": items})


def api_seats_for_show_timing(request, show_timing_id):
    show_timing = get_object_or_404(ShowTiming, pk=show_timing_id)
    seats = list(
        Seat.objects.filter(venue=show_timing.venue).values("id", "seat_number", "category", "price")
    )
    return JsonResponse({"seats": seats})


def validate_coupon_api(request):
    code = request.GET.get("coupon")
    amount = float(request.GET.get("amount", 0))
    result = validate_coupon(code, amount)
    return JsonResponse(result)
