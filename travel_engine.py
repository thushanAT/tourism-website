# L.Y.S.S. Iduranga  24IT0478 (1 - 47)
from datetime import datetime

def generate_seasonal_itinerary(arrival_date_str, total_days):
    try:
        #  Guest input Date 
        arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d')
        month = arrival_date.month
    except Exception:
        month = datetime.now().month

    total_days = int(total_days)
    
    # everyday available places (Cultural & Heritage / Nature)
    all_weather_destinations = [
        "Sigiriya Ancient Rock Fortress",
        "Kandy Temple of the Tooth Relic",
        "Dambulla Golden Cave Temple",
        "Ella (Nine Arch Bridge & Little Adams Peak)",
        "Nuwara Eliya Tea Gardens & Waterfalls",
        "Anuradhapura Sacred Ancient City",
        "Polonnaruwa Historical Ruins",
        "Udawalawe National Park (Elephant Transit Home)"
    ]

    # seasonal destinations
    # November - April - southern , western
    if month in [11, 12, 1, 2, 3, 4]:
        seasonal_destinations = [
            "Mirissa Beach (Whale Watching Season)",
            "Hikkaduwa (Coral Reef & Beach)",
            "Galle Dutch Fort",
            "Yala National Park Safari (Best Wildlife spotting season)",
            "Bentota Golden Beach"
        ]
        season_name = "South & West Coast Peak Season (Sunny Beach & Blue Whale Watching)"
    
    # may - october - East beach
    else:
        seasonal_destinations = [
            "Trincomalee (Nilaveli Beach & Pigeon Island)",
            "Arugam Bay (World famous Surfing Point)",
            "Pasikudah (Calm shallow bay)",
            "Minneriya National Park (The Great Elephant Gathering)",
            "Jaffna Peninsula (Nallur Temple & Islands)"
        ]
        season_name = "East Coast Peak Season (Perfect Blue Beach & Surfing)"
# A.T.Dinuka 24IT0465  (48 - 72)
    # 4. All Places Pool
    # create plan and check guest's date in Sri lanka
    full_route = all_weather_destinations + seasonal_destinations
    
    itinerary = []
    itinerary.append(f"💡 Detected Season: {season_name}")
    itinerary.append(f"📅 Tour Timeline: {total_days} Days Round Trip")
    itinerary.append("--------------------------------------------------")

    # 5. create root for 7, 14, 21 days
    for day in range(1, total_days + 1):
        # loop again if guest's date more than our plan
        place_index = (day - 1) % len(full_route)
        place = full_route[place_index]
        
        # daily plan
        if day == 1:
            itinerary.append(f"Day {day}: Arrival at BIA Colombo Airport ✈️ -> Transfer to Negombo Lagoon for rest.")
        elif day == total_days:
            itinerary.append(f"Day {day}: Colombo City Shopping & Souvenirs 🛍️ -> Departure to Airport.")
        else:
            itinerary.append(f"Day {day}: Explore {place} (Optimized for seasonal weather).")
            
    return itinerary