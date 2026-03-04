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

# 5. Run Server
if __name__ == '__main__':
    print("🚀 Aura Holidays API is running on http://127.0.0.1:5000")
    app.run(debug=True)