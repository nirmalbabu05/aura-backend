from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 1. App Setup
app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///holidays.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. Database Model
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)  
    title = db.Column(db.String(100), nullable=False)       
    duration = db.Column(db.String(20), nullable=False)     
    price = db.Column(db.String(20), nullable=False)        
    image = db.Column(db.String(100), nullable=False)       
    category = db.Column(db.String(50), default='General')
    overview = db.Column(db.Text, nullable=True)
    itinerary = db.Column(db.Text, nullable=True)
    inclusions = db.Column(db.String(200), nullable=True)

# 🌟 AUTOMATIC DATA SEEDING (BALI PACKAGE) 🌟
def seed_database():
    if Package.query.count() == 0:
        bali_itinerary = (
            "Day 1: Arrival in Paradise & Romantic Beach Walk\n"
            "Morning: Arrive at Denpasar Airport. Private transfer to Seminyak resort.\n"
            "Evening: Romantic stroll along Seminyak Beach followed by Balinese dinner.\n\n"
            "Day 2: Cultural Heart of Ubud & Swing Experience\n"
            "Morning: Visit Tegalalang Rice Terrace and try the iconic Bali Swing.\n"
            "Afternoon: Explore Ubud Monkey Forest and enjoy valley-view lunch.\n\n"
            "Day 3: Island Hopping to Nusa Penida\n"
            "Morning: Speed boat to Nusa Penida. Visit Kelingking Beach (T-Rex Bay).\n"
            "Afternoon: Relax at Broken Beach and Angel’s Billabong.\n\n"
            "Day 4: Temple Circuit & Sunset at Uluwatu\n"
            "Afternoon: Visit the majestic Uluwatu Temple on the cliff.\n"
            "Evening: Watch Kecak Fire Dance followed by seafood dinner at Jimbaran Bay.\n\n"
            "Day 5: Spa & Relaxation\n"
            "Morning: 2-hour Balinese Couple Spa and Flower Bath session.\n"
            "Evening: Farewell Sunset Dinner Cruise with live music.\n\n"
            "Day 6: Departure\n"
            "Morning: Visit Tanah Lot Temple (The Temple in the Sea).\n"
            "Afternoon: Private drop-off at Airport for departure."
        )
        
        bali_pkg = Package(
            destination="Bali",
            title="Bali Honeymoon Retreat",
            duration="5N/6D",
            price="45,000",
            image="bali,resort",
            category="Honeymoon",
            overview="Experience the ultimate romantic getaway in the 'Island of Gods'. Private villas, sunset dinners, and cultural wonders await.",
            inclusions="5 Nights Villa, Daily Breakfast, 2 Candlelight Dinners, Private Car, Spa Session, Airport Transfers",
            itinerary=bali_itinerary
        )
        db.session.add(bali_pkg)
        db.session.commit()
        print("✅ Bali Package Seeded Successfully!")

# Create tables and seed data
with app.app_context():
    db.create_all()
    seed_database()

# 3. API Routes (Consistently using same keys for Frontend)
@app.route('/api/packages/<destination>', methods=['GET'])
def get_packages(destination):
    packages = Package.query.filter_by(destination=destination).all()
    result = []
    for p in packages:
        result.append({
            "id": p.id, "n": p.title, "d": p.duration, 
            "p": p.price, "i": p.image, "over": p.overview, 
            "itin": p.itinerary, "inc": p.inclusions, "cat": p.category
        })
    return jsonify(result)

@app.route('/api/packages/all', methods=['GET'])
def get_all_packages():
    packages = Package.query.all()
    result = []
    for p in packages:
        result.append({
            "id": p.id, "destination": p.destination, "title": p.title, 
            "price": p.price, "duration": p.duration, "image": p.image,
            "category": p.category, "overview": p.overview, 
            "itinerary": p.itinerary, "inclusions": p.inclusions
        })
    return jsonify(result)

@app.route('/api/packages', methods=['POST'])
def add_package():
    data = request.json
    new_package = Package(
        destination=data['destination'], title=data['title'], duration=data['duration'],
        price=data['price'], image=data['image'], category=data.get('category', 'General'),
        overview=data.get('overview', ''), itinerary=data.get('itinerary', ''),
        inclusions=data.get('inclusions', '')
    )
    db.session.add(new_package)
    db.session.commit()
    return jsonify({"message": f"Successfully added {data['title']}!"}), 201

@app.route('/api/packages/<int:package_id>', methods=['PUT'])
def update_package(package_id):
    package = Package.query.get(package_id)
    if package:
        data = request.json
        package.destination = data['destination']
        package.title = data['title']
        package.duration = data['duration']
        package.price = data['price']
        package.image = data['image']
        package.category = data.get('category', 'General')
        package.overview = data.get('overview', '')
        package.itinerary = data.get('itinerary', '')
        package.inclusions = data.get('inclusions', '')
        db.session.commit()
        return jsonify({"message": f"Successfully updated {package.title}!"}), 200
    return jsonify({"message": "Package not found!"}), 404

@app.route('/api/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    package = Package.query.get(package_id)
    if package:
        db.session.delete(package)
        db.session.commit()
        return jsonify({"message": "Deleted successfully!"}), 200
    return jsonify({"message": "Not found!"}), 404

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin" and data.get('password') == "aura2026":
        return jsonify({"success": True, "message": "Login Successful!"}), 200
    return jsonify({"success": False, "message": "Invalid Credentials!"}), 401

@app.route('/api/chat', methods=['POST'])
def chat_assistant():
    try:
        data = request.json
        msg = data.get('message', '').lower()
        if any(w in msg for w in ['hi', 'hello', 'hey']):
            return jsonify({"reply": "Hello! 👋 I am the Aura AI Assistant. Tell me your dream destination!"})
        all_pkgs = Package.query.all()
        matched = [p for p in all_pkgs if p.destination.lower() in msg or p.title.lower() in msg]
        if matched:
            reply = "I found some amazing options! ✈️<br><br>"
            for p in matched[:3]: reply += f"🔹 <b>{p.title}</b> ({p.duration}) - ₹{p.price}<br>"
            return jsonify({"reply": reply})
        return jsonify({"reply": "Try asking about Paris, Bali, or Dubai!"})
    except:
        return jsonify({"reply": "Database error 🔄"}), 500

if __name__ == '__main__':
    app.run(debug=True)