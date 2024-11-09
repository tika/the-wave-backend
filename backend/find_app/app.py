from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timedelta, timezone
from math import radians

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/userPresenceDB"
mongo = PyMongo(app)


@app.route('/')
def index():
    return "MongoDB connected!"

@app.route('/api/register_presence', methods=['POST'])
def register_presence():
    data = request.json
    username = data["username"]
    location = data.get("location")
    preference = data.get("preference")

    print("Received data:", data)

    # Ensure latitude and longitude are provided
    if "latitude" not in location or "longitude" not in location:
        return jsonify({"error": "Location data missing"}), 400

    # Update or insert the user's presence data
    presence_data = {
        "username": username,
        "last_active": datetime.utcnow(),
        "preference": preference,
        "location": {
            "type": "Point",
            "coordinates": [location["longitude"], location["latitude"]]
        }
    }
    print("Saving presence data:", presence_data)

    result = mongo.db.users.update_one(
        {"username": username},
        {"$set": presence_data},
        upsert=True
    )
    print("MongoDB result:", result.modified_count, result.upserted_id)
    
    return jsonify({"message": "Presence updated"}), 200

@app.route('/api/nearby_users', methods=['GET'])
def get_nearby_users():
    # Expect user's current location as query parameters
    user_lat = float(request.args.get("latitude"))
    user_lon = float(request.args.get("longitude"))
    radius = 5  # Radius in miles

    # Convert radius to meters (MongoDB expects distance in meters)
    radius_in_meters = radius * 1609.34

    # Query for users within the specified radius using MongoDB's geospatial query
    nearby_users = mongo.db.users.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [user_lon, user_lat]
                },
                "$maxDistance": radius_in_meters
            }
        },
        # Optional: Filter to only get users active within the last 10 minutes
        "last_active": {"$gte": datetime.utcnow() - timedelta(minutes=10)}
    })

    # Prepare a list of nearby users to return
    user_list = []
    for user in nearby_users:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        user_list.append(user)

    return jsonify(user_list), 200
