from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from google import genai # PUTHU AI LIBRARY

# 1. App Setup
app = Flask(__name__)
CORS(app) 

# --- DATABASE CONFIGURATION ---
DATABASE_URL = "postgresql://postgres.ynpnuitpxbskgxzzojpw:G4L2xUnZzBVJxW21@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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

with app.app_context():
    db.create_all()

# --- AI CHATBOT SETUP (NEW SDK) ---
client = genai.Client(api_key="AIzaSyBzeSFIHY5jOtL7eu_BFny6gR_GCE-6-wQ") 

# 3. API Routes
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

# 🌟 THE SMART AI CHAT ROUTE (RAG IMPLEMENTATION) 🌟
# Ithu thaan orey oru chat route! Pazhaiyathu ellam thookiyachu!
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"reply": "Please say something!"}), 400

        # Fetch all packages to give AI context
        packages = Package.query.all()
        
        if packages:
            pkg_list = "\n".join([f"- {p.title} ({p.destination}): {p.duration} for ₹{p.price}" for p in packages])
            db_context = f"Here is our live database of packages:\n{pkg_list}\n\nRule: ONLY recommend packages from this list. Do not make up packages."
        else:
            db_context = "Currently, no packages are available."

        system_prompt = f"You are a friendly AI travel assistant for Aura Holidays. Keep your answers short (2-3 sentences max) and enthusiastic.\n\n{db_context}"
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\nAI:"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"reply": "Sorry, my AI brain is taking a quick nap! Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True)