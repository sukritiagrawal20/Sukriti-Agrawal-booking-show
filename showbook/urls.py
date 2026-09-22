from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("bookings/", include("bookings.urls")),
    path("payments/", include("payments.urls")),
    path("api/", include("shows.api_urls")),
    path("api/bookings/", include("bookings.api_urls")),
    path("api/payment/", include("payments.api_urls")),
    path("", include("shows.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
