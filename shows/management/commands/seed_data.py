from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
from bookings.models import Coupon
from shows.models import Seat, Show, ShowTiming, Venue


class Command(BaseCommand):
    help = "Seed demo data for ShowBook"

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.filter(username="demo").delete()
        User.objects.create_user(username="demo", email="demo@example.com", password="demo123", first_name="Demo", last_name="User")

        venue_data = [
            ("PVR Jaipur", "Malviya Nagar, Jaipur", "Jaipur", 200),
            ("INOX Jaipur", "C Scheme, Jaipur", "Jaipur", 180),
            ("Raj Mandir Cinema", "Bhagat Singh Marg, Jaipur", "Jaipur", 220),
            ("INOX Delhi", "Saket, Delhi", "Delhi", 180),
            ("Cinepolis Mumbai", "Andheri East, Mumbai", "Mumbai", 220),
            ("PVR Bangalore", "Indiranagar, Bangalore", "Bangalore", 160),
            ("Prasads Hyderabad", "Madhapur, Hyderabad", "Hyderabad", 250),
            ("PVR Pune", "Kalyani Nagar, Pune", "Pune", 190),
            ("INOX Kolkata", "Salt Lake, Kolkata", "Kolkata", 180),
            ("PVR Chennai", "Anna Nagar, Chennai", "Chennai", 200),
            ("Grand Arena Ahmedabad", "SG Highway, Ahmedabad", "Ahmedabad", 210),
        ]
        venues = []
        for name, address, city, capacity in venue_data:
            venue, _ = Venue.objects.get_or_create(name=name, defaults={"address": address, "city": city, "capacity": capacity, "seat_layout": "A1-A10"})
            venues.append(venue)

        show_data = [
            ("Avengers: Endgame", "Marvel action epic", "Movie", "Action", "English", 180, 4.8, "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=700&q=85"),
            ("Pathaan", "Spy thriller", "Movie", "Action", "Hindi", 146, 4.7, "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=700&q=85"),
            ("Jawan", "Mass action entertainer", "Movie", "Action", "Hindi", 169, 4.6, "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=700&q=85"),
            ("Dune: Part Two", "Sci-fi saga", "Movie", "Sci-Fi", "English", 166, 4.9, "https://images.unsplash.com/photo-1440404653325-ab127d490017?auto=format&fit=crop&w=700&q=85"),
            ("The Intern", "Business comedy", "Show", "Comedy", "English", 120, 4.2, "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=700&q=85"),
            ("Midnight in Mumbai", "A neon-soaked city mystery", "Movie", "Thriller", "Hindi", 132, 4.5, "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=700&q=85"),
            ("Laugh Out Loud", "A night of live stand-up comedy", "Event", "Comedy", "English", 110, 4.4, "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?auto=format&fit=crop&w=700&q=85"),
            ("The Grand Stage", "A spectacular live theatre production", "Event", "Drama", "English", 150, 4.7, "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=700&q=85"),
            ("Sound & Light Festival", "Live music under the city lights", "Event", "Music", "English", 180, 4.6, "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=700&q=85"),
            ("3 Idiots", "A friendship story that changed a generation", "Movie", "Drama", "Hindi", 170, 4.8, "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=701&q=85"),
            ("Interstellar", "A journey beyond the stars", "Movie", "Sci-Fi", "English", 169, 4.9, "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=700&q=85"),
            ("Inception", "Dreams within dreams", "Movie", "Thriller", "English", 148, 4.8, "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=700&q=85"),
            ("Animal", "A fierce family drama", "Movie", "Drama", "Hindi", 204, 4.3, "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=700&q=85"),
            ("Pushpa 2", "The rule continues", "Movie", "Action", "Telugu", 180, 4.6, "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=701&q=85"),
            ("Oppenheimer", "The story of an invention that changed history", "Movie", "Drama", "English", 180, 4.7, "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=700&q=85"),
            ("Arijit Singh Live", "An intimate evening of music", "Show", "Music", "Hindi", 140, 4.9, "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=700&q=85"),
            ("Hamlet", "Shakespeare under a new light", "Show", "Drama", "English", 145, 4.5, "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=701&q=85"),
            ("Comedy Nights", "Stand-up from the country's sharpest voices", "Show", "Comedy", "Hindi", 100, 4.6, "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?auto=format&fit=crop&w=701&q=85"),
            ("Bollywood Night", "Dance, music, and all-time favourites", "Event", "Music", "Hindi", 160, 4.4, "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=701&q=85"),
            ("Cricket Premier League", "The city meets under floodlights", "Event", "Sports", "English", 210, 4.7, "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=700&q=85"),
            ("Football Derby", "A night of rivalry and roaring stands", "Event", "Sports", "English", 120, 4.5, "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=700&q=85"),
            ("EDM Night", "Electronic music and immersive lights", "Event", "Concerts", "English", 180, 4.5, "https://images.unsplash.com/photo-1571266028243-d220c9c3b4c8?auto=format&fit=crop&w=700&q=85"),
            ("Drama Festival", "Three plays, one unforgettable weekend", "Event", "Drama", "English", 180, 4.3, "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=702&q=85"),
            ("Kalki 2898 AD", "A futuristic mythic adventure", "Movie", "Sci-Fi", "Telugu", 180, 4.6, "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=700&q=85"),
            ("The Dark Knight", "A hero faces a new kind of chaos", "Movie", "Action", "English", 152, 4.9, "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?auto=format&fit=crop&w=700&q=85"),
            ("Rockstar", "A musician finds his true voice", "Movie", "Music", "Hindi", 159, 4.5, "https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=700&q=85"),
            ("Barbie", "A colorful trip beyond the ordinary", "Movie", "Comedy", "English", 114, 4.2, "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=700&q=85"),
            ("The Musical Night", "A live orchestra and vocal showcase", "Show", "Music", "English", 125, 4.4, "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?auto=format&fit=crop&w=700&q=85"),
            ("The Great Debate", "Ideas, stories, and brilliant speakers", "Show", "Drama", "English", 95, 4.1, "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=700&q=85"),
            ("Improv League", "Unscripted comedy made with the audience", "Show", "Comedy", "English", 90, 4.5, "https://images.unsplash.com/photo-1527224857830-43a7acc85260?auto=format&fit=crop&w=700&q=85"),
            ("Kathak Evening", "A classical dance performance", "Show", "Drama", "Hindi", 110, 4.3, "https://images.unsplash.com/photo-1547153760-18fc86324498?auto=format&fit=crop&w=700&q=85"),
            ("Acoustic Stories", "Songwriters share the stories behind their songs", "Show", "Music", "English", 100, 4.2, "https://images.unsplash.com/photo-1521337581100-8ca9a73a5f79?auto=format&fit=crop&w=700&q=85"),
            ("Magic After Dark", "A theatrical night of impossible illusions", "Show", "Drama", "English", 105, 4.1, "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=702&q=85"),
            ("City Marathon", "Run together through the city", "Event", "Sports", "English", 180, 4.4, "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=700&q=85"),
            ("Campus Carnival", "Food, music, games, and workshops", "Event", "Cultural", "English", 240, 4.2, "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&w=700&q=85"),
        ]
        shows = []
        for title, description, category, genre, language, duration, rating, poster_url in show_data:
            show, _ = Show.objects.get_or_create(title=title, defaults={"description": description, "category": category, "genre": genre, "language": language, "duration": duration, "rating": rating, "poster_url": poster_url})
            if not show.poster_url:
                show.poster_url = poster_url
                show.save(update_fields=["poster_url"])
            shows.append(show)

        for index, show in enumerate(shows):
            venue = venues[index % len(venues)]
            ShowTiming.objects.get_or_create(
                show=show,
                venue=venue,
                date="2026-09-25",
                start_time="10:00:00",
                end_time="12:30:00",
            )

            for row in ["A", "B", "C"]:
                for num in range(1, 6):
                    Seat.objects.get_or_create(venue=venue, seat_number=f"{row}{num}", defaults={"category": "Regular", "price": 500})

        Coupon.objects.get_or_create(code="WELCOME10", defaults={"discount_type": "percent", "discount_value": 10, "minimum_amount": 500, "expiry_date": "2027-12-31", "usage_limit": 10, "active": True})
        Coupon.objects.get_or_create(code="FIRSTBOOK", defaults={"discount_type": "flat", "discount_value": 100, "minimum_amount": 800, "expiry_date": "2027-12-31", "usage_limit": 5, "active": True})

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
