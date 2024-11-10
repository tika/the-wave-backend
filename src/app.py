import os
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from geopy.distance import geodesic
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/userDB"
# mongo = PyMongo(app)
# MongoDB Atlas URI
# MongoDB URI from environment variables
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

# Test MongoDB connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Access your database and collection
db = client.get_database("userDB")
users_collection = db.users

# Create index only once during app initialization
def init_indexes():
    # Check if index already exists
    existing_indexes = users_collection.list_indexes()
    index_exists = False
    for index in existing_indexes:
        if "location_2dsphere" in index["name"]:
            index_exists = True
            break

    # Create only if it doesn't exist
    if not index_exists:
        users_collection.create_index([("location", "2dsphere")])

# Initialize indexes when app starts
with app.app_context():
    init_indexes()

@app.route('/')
def index():
    return "MongoDB connected!"

@app.route('/api/location', methods=['POST'])
def register_presence():
    data = request.json
    user_id = data["userID"]
    location = data.get("location")
    preference = data.get("preference")
    emoji = data.get("emoji")

    print("Received data:", data)

   # Validate location data
    if not location or not isinstance(location, dict):
        return jsonify({"error": "Location data is required"}), 400

    longitude = location.get("longitude")
    latitude = location.get("latitude")
    print("5. coordinates:", longitude, latitude)  # Debug print

    if longitude is None or latitude is None:
        return jsonify({"error": "Both longitude and latitude are required"}), 400

    try:
        longitude = float(longitude)
        latitude = float(latitude)

        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            return jsonify({
                "error": "Invalid coordinates. Longitude must be between -180 and 180, Latitude between -90 and 90"
            }), 400

    except (ValueError, TypeError):
        return jsonify({"error": "Coordinates must be valid numbers"}), 400

    # Update or insert the user's presence data
    presence_data = {
        "userID": user_id,
        "last_active": datetime.utcnow(),
        "preference": preference,
        "emoji": emoji,
        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }
    }
    print("Saving presence data:", presence_data)

    result = users_collection.update_one(
        {"userID": user_id},
        {"$set": presence_data},
        upsert=True
    )
    print("MongoDB result:", result.modified_count, result.upserted_id)

    # Expect user's current location as query parameters
    user_lon = longitude
    user_lat = latitude
    SEARCH_RADIUS_MILES = 5  # Radius in miles

    # Convert radius to meters (MongoDB expects distance in meters)
    radius_in_meters = SEARCH_RADIUS_MILES * 1609.34

    # Query for users within the specified radius using MongoDB's geospatial query
    nearby_users = users_collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [user_lon, user_lat]
                },
                "$maxDistance": radius_in_meters
            }
        },
        "last_active": {"$gte": datetime.utcnow() - timedelta(minutes=10)}
    })
    print("6. nearby_users:", nearby_users)  # Debug print

    # Prepare a list of nearby users to return
    loc_list = [{"location": user["location"]["coordinates"]} for user in nearby_users]

    return jsonify(loc_list), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
