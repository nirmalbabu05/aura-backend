from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 1. App Setup
app = Flask(__name__)
CORS(app) # Allows your HTML file to communicate with this Python server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///holidays.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. Database Model (Blueprint for a Tour Package)
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)  # e.g., 'Bali'
    title = db.Column(db.String(100), nullable=False)       # e.g., 'Bali Honeymoon Retreat'
    duration = db.Column(db.String(20), nullable=False)     # e.g., '5N/6D'
    price = db.Column(db.String(20), nullable=False)        # e.g., '45,000'
    image = db.Column(db.String(100), nullable=False)       # e.g., 'bali,resort'

# Create the database file
with app.app_context():
    db.create_all()

# 3. API Route: Get packages for a specific destination
@app.route('/api/packages/<destination>', methods=['GET'])
def get_packages(destination):
    packages = Package.query.filter_by(destination=destination).all()
    result = []
    for p in packages:
        result.append({
            "id": p.id, "n": p.title, "d": p.duration, 
            "p": p.price, "i": p.image
        })
    return jsonify(result)

# 4. API Route: Add a new package (Admin use)
@app.route('/api/packages', methods=['POST'])
def add_package():
    data = request.json
    new_package = Package(
        destination=data['destination'],
        title=data['title'],
        duration=data['duration'],
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_package)
    db.session.commit()
    return jsonify({"message": f"Successfully added {data['title']} to database!"}), 201

# --- PUTHU ROUTES FOR ADMIN PANEL ---

# Get ALL packages (Admin use & Homepage use)
@app.route('/api/packages/all', methods=['GET'])
def get_all_packages():
    packages = Package.query.all()
    result = []
    for p in packages:
        result.append({
            "id": p.id, "destination": p.destination, "title": p.title, 
            "price": p.price, "duration": p.duration, "image": p.image
        })
    return jsonify(result)

# Delete a package by ID (Admin use)
@app.route('/api/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    package = Package.query.get(package_id)
    if package:
        db.session.delete(package)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted {package.title}!"}), 200
    return jsonify({"message": "Package not found!"}), 404


# Update/Edit a package by ID (Admin use)
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
        db.session.commit()
        return jsonify({"message": f"Successfully updated {package.title}!"}), 200
    return jsonify({"message": "Package not found!"}), 404


# --- ADMIN LOGIN ROUTE ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Ungalukku pudicha username & password set pannunga
    if username == "admin" and password == "aura2026":
        return jsonify({"success": True, "message": "Login Successful!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid Credentials!"}), 401

# --- AURA AI CHATBOT ROUTE 🧠 ---
@app.route('/api/chat', methods=['POST'])
def chat_assistant():
    try:
        data = request.json
        user_message = data.get('message', '').lower()

        # 1. Basic Greetings
        if any(word in user_message for word in ['hi', 'hello', 'hey', 'help', 'start']):
            return jsonify({"reply": "Hello! 👋 I am the Aura AI Assistant. Tell me your dream destination (e.g., 'I want to go to Bali' or 'Do you have Paris packages?')."})

        # 2. Fetch all real packages from the Database
        all_packages = Package.query.all()

        # 3. Simple Rule-Based NLP Logic
        matched_packages = []
        for pkg in all_packages:
            if pkg.destination.lower() in user_message or pkg.title.lower() in user_message:
                matched_packages.append(pkg)

        # 4. Construct AI Response
        if matched_packages:
            reply = "I found some amazing options for you! ✈️<br><br>"
            for p in matched_packages[:3]: # Shows top 3 matches to keep chat clean
                reply += f"🔹 <b>{p.title}</b> ({p.duration}) - Starts at ₹{p.price}<br>"
            reply += "<br>You can click 'Enquire Now' at the top to book these!"
            return jsonify({"reply": reply})

        # 5. Fallback Response
        return jsonify({"reply": "I'm still learning! 🤖 I couldn't find a specific package for that right now. Try asking about our popular spots like <b>Paris, Bali, or Dubai</b>!"})

    except Exception as e:
        return jsonify({"reply": "Oops! My database brain is currently syncing. Try again in a minute! 🔄"}), 500

# 5. Run Server
if __name__ == '__main__':
    print("🚀 Aura Holidays API is running on http://127.0.0.1:5000")
    app.run(debug=True)