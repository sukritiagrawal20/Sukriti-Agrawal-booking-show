from django.urls import path

from . import views

urlpatterns = [
    path("create-order/<str:booking_id>/", views.create_payment_order, name="payment_create"),
    path("verify/", views.verify_payment, name="payment_verify"),
    path("api/create-order/", views.api_create_order, name="api_payment_create_order"),
    path("api/verify/", views.api_verify_payment, name="api_payment_verify"),
]
