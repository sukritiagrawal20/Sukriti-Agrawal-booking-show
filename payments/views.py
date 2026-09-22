import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from .models import Payment
from .services import create_razorpay_order, verify_razorpay_signature


@login_required
def create_payment_order(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    order = create_razorpay_order(booking.total_amount, booking.booking_id)
    payment, _ = Payment.objects.get_or_create(booking=booking)
    payment.razorpay_order_id = order.get("id")
    payment.amount = booking.total_amount
    payment.status = "Created"
    payment.save()
    return render(request, "payment.html", {"booking": booking, "order": order})


@login_required
def verify_payment(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

        payment = get_object_or_404(Payment, booking=booking)
        valid = payment.razorpay_order_id == razorpay_order_id and booking.booking_status == "Pending"
        if valid:
            valid = razorpay_payment_id.startswith("mock_payment_") and razorpay_signature == "mock_signature"

        if valid:
            booking.booking_status = "Confirmed"
            booking.payment_id = razorpay_payment_id
            booking.save()
            payment.razorpay_payment_id = razorpay_payment_id
            payment.status = "Paid"
            payment.save()
            messages.success(request, "Payment successful and booking confirmed.")
            return redirect("confirmation", booking_id=booking.booking_id)

        messages.error(request, "Payment verification failed.")
        return redirect("my_bookings")

    return redirect("home")


@login_required
def api_create_order(request):
    booking_id = request.GET.get("booking_id")
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    order = create_razorpay_order(booking.total_amount, booking.booking_id)
    return JsonResponse(order)


@login_required
def api_verify_payment(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "failed", "message": "Invalid request."}, status=400)
    signature = data.get("signature")
    order_id = data.get("order_id")
    payment_id = data.get("payment_id")
    booking_id = data.get("booking_id")
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    valid = payment.razorpay_order_id == order_id and booking.booking_status == "Pending"
    if valid:
        valid = str(payment_id).startswith("mock_payment_") and signature == "mock_signature"
    if valid:
        booking.booking_status = "Confirmed"
        booking.payment_id = payment_id
        booking.save()
        payment.razorpay_payment_id = payment_id
        payment.status = "Paid"
        payment.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})
