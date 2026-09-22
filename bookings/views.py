import json
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from payments.models import Payment
from shows.models import Seat, ShowTiming
from .models import BookedSeat, Booking, Coupon
from .services import generate_booking_id, validate_coupon


@login_required
def create_booking(request, show_timing_id):
    show_timing = get_object_or_404(ShowTiming, pk=show_timing_id)
    if request.method == "POST":
        selected = request.POST.getlist("seat")
        if not selected:
            messages.error(request, "Pick at least one seat.")
            return redirect("select_seats", show_timing_id=show_timing.id)

        with transaction.atomic():
            seats = list(Seat.objects.filter(venue=show_timing.venue, seat_number__in=selected))
            if len(seats) != len(set(selected)) or len(selected) != len(set(selected)):
                messages.error(request, "One or more selected seats are invalid.")
                return redirect("select_seats", show_timing_id=show_timing.id)
            for seat in seats:
                exists = BookedSeat.objects.filter(
                    seat=seat,
                    booking__show_timing=show_timing,
                    booking__booking_status__in=["Confirmed", "Pending"],
                ).exists()
                if exists:
                    messages.error(request, f"Seat {seat.seat_number} has already been booked.")
                    return redirect("select_seats", show_timing_id=show_timing.id)

            booking = Booking.objects.create(
                user=request.user,
                show_timing=show_timing,
                booking_id=generate_booking_id(),
                total_amount=Decimal(str(sum(float(seat.price) for seat in seats) + 30 * len(seats) + 20 * len(seats))),
                discount=0,
                booking_status="Pending",
            )
            for seat in seats:
                BookedSeat.objects.create(booking=booking, seat=seat, price=seat.price)

            request.session["pending_booking_id"] = booking.booking_id
            return redirect("payment_create", booking_id=booking.booking_id)

    return redirect("select_seats", show_timing_id=show_timing.id)


@login_required
def apply_coupon(request):
    code = request.POST.get("code", "")
    booking_id = request.POST.get("booking_id")
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    result = validate_coupon(code, float(booking.total_amount))
    if result["valid"]:
        booking.discount = Decimal(str(result["discount"]))
        booking.total_amount = Decimal(str(float(booking.total_amount) - result["discount"]))
        booking.save()
        messages.success(request, "Coupon applied successfully.")
    else:
        messages.error(request, result["message"])
    return redirect("booking_summary", show_timing_id=booking.show_timing_id)


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, "booking_detail.html", {"booking": booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if request.method != "POST":
        messages.error(request, "Cancellation must be confirmed from the booking page.")
        return redirect("my_bookings")
    if booking.booking_status in {"Cancelled", "Refunded"}:
        messages.info(request, "This booking is already cancelled.")
        return redirect("my_bookings")

    booking.booking_status = "Cancelled"
    booking.save()
    booking.booked_seats.all().delete()
    messages.success(request, "Booking cancelled and seats released.")
    return redirect("my_bookings")


# API views

@login_required
def api_bookings(request):
    bookings = Booking.objects.filter(user=request.user).values(
        "id", "booking_id", "show_timing__show__title", "booking_status", "total_amount"
    )
    return JsonResponse({"bookings": list(bookings)})


@login_required
def api_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return JsonResponse({
        "booking_id": booking.booking_id,
        "amount": str(booking.total_amount),
        "status": booking.booking_status,
    })


@login_required
def api_coupon_validate(request):
    code = request.GET.get("code")
    order_amount = float(request.GET.get("amount", 0))
    result = validate_coupon(code, order_amount)
    return JsonResponse(result)
