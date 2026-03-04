from app import app, db, Package

# MASSIVE REAL-WORLD TRAVEL PACKAGES DATABASE
packages_data = [
    # --- ASIA ---
    {"destination": "Bali", "title": "Bali Honeymoon Retreat", "duration": "5N / 6D", "price": "45,000", "image": "bali"},
    {"destination": "Bali", "title": "Nusa Penida & Ubud Escapade", "duration": "6N / 7D", "price": "58,000", "image": "ubud"},
    {"destination": "Bali", "title": "Luxury Pool Villa Stay", "duration": "4N / 5D", "price": "65,000", "image": "villa"},
    {"destination": "Dubai", "title": "Dubai Desert Safari & City Tour", "duration": "4N / 5D", "price": "48,000", "image": "dubai"},
    {"destination": "Dubai", "title": "Premium Dubai with Burj Khalifa", "duration": "5N / 6D", "price": "62,000", "image": "burjkhalifa"},
    {"destination": "Dubai", "title": "Dubai Shopping Festival Special", "duration": "4N / 5D", "price": "55,000", "image": "shopping"},
    {"destination": "Singapore", "title": "Singapore City & Sentosa", "duration": "4N / 5D", "price": "55,000", "image": "singapore"},
    {"destination": "Singapore", "title": "Universal Studios Family Trip", "duration": "5N / 6D", "price": "68,000", "image": "sentosa"},
    {"destination": "Thailand", "title": "Phuket & Krabi Beach Tour", "duration": "5N / 6D", "price": "42,000", "image": "phuket"},
    {"destination": "Thailand", "title": "Bangkok City Explorer", "duration": "3N / 4D", "price": "28,000", "image": "bangkok"},

    # --- EUROPE ---
    {"destination": "Paris", "title": "Eiffel Tower Romance", "duration": "4N / 5D", "price": "1,10,000", "image": "paris"},
    {"destination": "Paris", "title": "Disneyland Paris Family Special", "duration": "5N / 6D", "price": "1,35,000", "image": "disneyland"},
    {"destination": "France", "title": "French Riviera Luxury Tour", "duration": "6N / 7D", "price": "1,65,000", "image": "france"},
    {"destination": "Switzerland", "title": "Swiss Alps Premium", "duration": "6N / 7D", "price": "1,45,000", "image": "switzerland"},
    {"destination": "Switzerland", "title": "Zurich & Interlaken Getaway", "duration": "5N / 6D", "price": "1,25,000", "image": "zurich"},
    {"destination": "Italy", "title": "Rome, Venice & Florence", "duration": "7N / 8D", "price": "1,55,000", "image": "rome"},
    {"destination": "Italy", "title": "Amalfi Coast Romantic Drive", "duration": "5N / 6D", "price": "1,30,000", "image": "venice"},
    {"destination": "London", "title": "London City Heritage Tour", "duration": "4N / 5D", "price": "1,15,000", "image": "london"},

    # --- ISLANDS ---
    {"destination": "Maldives", "title": "Maldives Ocean Water Villa", "duration": "3N / 4D", "price": "85,000", "image": "maldives"},
    {"destination": "Maldives", "title": "Premium Maldives Honeymoon", "duration": "4N / 5D", "price": "1,15,000", "image": "ocean"},
    {"destination": "Maldives", "title": "Family Beach Resort Stay", "duration": "4N / 5D", "price": "95,000", "image": "beach"},
    {"destination": "Mauritius", "title": "Mauritius Island Hopping", "duration": "5N / 6D", "price": "78,000", "image": "mauritius"},
    {"destination": "Mauritius", "title": "Mauritius Honeymoon Package", "duration": "6N / 7D", "price": "92,000", "image": "island"},

    # --- NORTH INDIA ---
    {"destination": "Agra", "title": "Taj Mahal & Golden Triangle", "duration": "4N / 5D", "price": "22,000", "image": "tajmahal"},
    {"destination": "Kashmir", "title": "Srinagar & Gulmarg Snow Tour", "duration": "5N / 6D", "price": "32,000", "image": "kashmir"},
    {"destination": "Kashmir", "title": "Kashmir Dal Lake Houseboat", "duration": "4N / 5D", "price": "28,000", "image": "shikara"},
    {"destination": "Manali", "title": "Kullu Manali Snow Adventure", "duration": "5N / 6D", "price": "18,500", "image": "manali"},
    {"destination": "Manali", "title": "Rohtang Pass Explorer", "duration": "4N / 5D", "price": "16,000", "image": "mountains"},

    # --- SOUTH INDIA ---
    {"destination": "Kerala", "title": "Munnar & Alleppey Backwaters", "duration": "4N / 5D", "price": "18,500", "image": "kerala"},
    {"destination": "Kerala", "title": "God's Own Country Explorer", "duration": "6N / 7D", "price": "26,000", "image": "munnar"},
    {"destination": "Kerala", "title": "Wayanad Nature Retreat", "duration": "3N / 4D", "price": "14,000", "image": "wayanad"},
    {"destination": "Ooty", "title": "Ooty & Coonoor Heritage Train", "duration": "3N / 4D", "price": "12,500", "image": "ooty"},
    {"destination": "Kodaikanal", "title": "Kodaikanal Pine Forest Stay", "duration": "3N / 4D", "price": "11,000", "image": "kodaikanal"},

    # --- WEST INDIA & WEDDING VENUES ---
    {"destination": "Goa", "title": "North Goa Party Getaway", "duration": "3N / 4D", "price": "14,500", "image": "goa"},
    {"destination": "Goa", "title": "South Goa Luxury Retreat", "duration": "4N / 5D", "price": "22,000", "image": "resort"},
    {"destination": "Goa", "title": "Goa Destination Wedding Package", "duration": "2N / 3D", "price": "5,50,000", "image": "wedding"},
    {"destination": "Rajasthan", "title": "Jaipur & Jodhpur Royal Tour", "duration": "6N / 7D", "price": "38,000", "image": "rajasthan"},
    {"destination": "Udaipur", "title": "Udaipur Palace Stay", "duration": "3N / 4D", "price": "28,000", "image": "udaipur"},
    {"destination": "Udaipur", "title": "Royal Udaipur Wedding Setup", "duration": "3N / 4D", "price": "8,00,000", "image": "palace"},

    # --- SPECIAL / OTHERS ---
    {"destination": "Andaman", "title": "Havelock Island Scuba Tour", "duration": "5N / 6D", "price": "35,000", "image": "andaman"},
    {"destination": "Andaman", "title": "Port Blair & Neil Island", "duration": "6N / 7D", "price": "42,000", "image": "scuba"}
]

with app.app_context():
    # Warning: This clears old data and loads the massive new list
    db.drop_all()
    db.create_all()
    
    for p in packages_data:
        new_pkg = Package(
            destination=p['destination'], 
            title=p['title'], 
            duration=p['duration'], 
            price=p['price'], 
            image=p['image']
        )
        db.session.add(new_pkg)
    
    db.session.commit()
    print(f"🔥 MEGA UPDATE: {len(packages_data)} Real Packages successfully injected into the Database! 🔥")