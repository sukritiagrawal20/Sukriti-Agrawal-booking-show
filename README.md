# ShowBook – Online Show & Event Ticket Booking System

ShowBook is a Django-based ticket booking platform for movies, live shows, concerts, and events. The project is designed as a functional B.Tech level application with authentication, seat booking, coupons, mock Razorpay integration, PDF ticket generation, QR codes, REST APIs, and an administrative dashboard.

## Features

- Responsive homepage with trending shows, events, venues, and search
- User registration/login/logout and profile management
- Search and filter by city, category, language, date, and price
- Show details and venue detail pages
- Interactive seat selection with booking validation
- Coupon application and invoice summary
- Mock/real Razorpay order creation and verification flow
- Booking confirmation with QR code and downloadable PDF ticket
- User booking dashboard for upcoming, past, and cancelled bookings
- Admin dashboard for show, venue, timing, booking, user, and coupon management
- Django REST API endpoints for mobile and front-end integrations

## Tech Stack

- Python 3
- Django
- Django REST Framework
- SQLite (development)
- Bootstrap 5
- ReportLab
- Pillow
- qrcode
- Razorpay

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:
   - python -m venv .venv
   - source .venv/bin/activate
3. Install dependencies:
   - pip install -r requirements.txt
4. Create environment file (.env) with the values listed below.
5. Run migrations:
   - python manage.py migrate
6. Create a superuser:
   - python manage.py createsuperuser
7. Load sample data:
   - python manage.py seed_data
8. Start the server:
   - python manage.py runserver

## Environment Variables

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
RAZORPAY_KEY_ID=rzp_test_xxxxxx
RAZORPAY_KEY_SECRET=your-secret
```

## Sample Data

Run:

```bash
python manage.py seed_data
```

This seeds multiple movies, venues, dates, seat categories, and sample coupons.

## Admin Panel

Open:

```text
http://127.0.0.1:8000/admin/
```

## API Endpoints

- /api/shows/
- /api/shows/<id>/
- /api/venues/
- /api/showtimes/
- /api/seats/<show_timing_id>/
- /api/bookings/
- /api/bookings/<id>/
- /api/coupons/validate/
- /api/payment/create-order/
- /api/payment/verify/

## Booking Flow

Home → select city/show → venue → date → timing → seat selection → checkout → payment → confirmation → ticket download.

## Notes

This project uses a mock/payment fallback if test keys are not configured so the app can run locally without a real Razorpay account. For actual production use, configure valid Razorpay keys in the .env file.
