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
db = client.get_database("the-wave-db")
users_collection = db.users
ripples_collection = db.ripples

# Create index only once during app initialization
def init_indexes():
    # Check if index already exists
    # Use location stuff in mongodb
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
    location = data.get("location")
    user_id = data.get("userID") # Get user id from body of request
    party_mode = data.get("partyMode") # Party mode = do we create ripples

    # If there is no location or the location type is invalid, return an error
    if not location or not isinstance(location, dict):
        return jsonify({"error": "Location data is required"}), 400

    longitude = location.get("longitude")
    latitude = location.get("latitude")
 
    # If longitude or latitude is missing, return an error
    if longitude is None or latitude is None:
        return jsonify({"error": "Both longitude and latitude are required"}), 400
    
    try:
        longitude = float(longitude)
        latitude = float(latitude)
    except (ValueError, TypeError):
        return jsonify({"error": "Coordinates must be valid numbers"}), 400

    # Update or insert user's presence data
    presence_data = {
        "userID": user_id,
        # "last_active": datetime.datetime(), # used for invalidation
        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }
    }

    # 2. Find all ripples near me (5km)
    user_location = (latitude, longitude)
    ripples_nearby = list(ripples_collection.find({
        "center": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": 5000  # 5000 meters
            }
        }
    }))

    # If no party mode, return nearby ripples
    if not party_mode:
        return jsonify({"nearbyRipples": ripples_nearby}), 200

    # If user is in party mode, update user's presence data
    users_collection.update_one(
        {"userID": user_id},
        {"$set": presence_data},
        upsert=True
    )

    # Check if I am in a ripple
    is_in_ripple = ripples_collection.find_one({"members": user_id})
    
    if is_in_ripple:
        # Further than 150m away from the origin of the ripple?
        distance = geodesic(user_location, tuple(is_in_ripple["origin"]["coordinates"])).meters
        if distance > 150:
            ripples_collection.update_one(
                {"_id": is_in_ripple["_id"]},
                {"$pull": {"members": user_id}}
            )

            # If there is now less than 3 people in the ripple, dissolve the ripple
            if len(is_in_ripple["members"]) < 3:
                ripples_collection.delete_one({"_id": is_in_ripple["_id"]})

            return jsonify({"message": "Left ripple", "nearbyRipples": ripples_nearby}), 200

        return jsonify({"message": "Already in a ripple", "nearbyRipples": ripples_nearby}), 200


    # If there are 3 or more users are within 30 meters of eachother and none of them are in a ripple
    # Make a ripple, with the center of the ripple being the average of the users' locations
    # and add the users to the ripple
    nearby_users = list(users_collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": 30  # 30 meters for new ripple
            }
        },
    }))

    if len(nearby_users) >= 3:
        # Calculate center of new ripple
        avg_lat = sum(user["location"]["coordinates"][1] for user in nearby_users) / len(nearby_users)
        avg_lon = sum(user["location"]["coordinates"][0] for user in nearby_users) / len(nearby_users)
        # use time mongodb, not datetime.datetime()
        new_ripple = {
            "center": {"type": "Point", "coordinates": [avg_lon, avg_lat]},
            "members": [user["userID"] for user in nearby_users],
        }
        ripple_id = ripples_collection.insert_one(new_ripple).inserted_id
        return jsonify({"message": "New ripple created", "ripple_id": str(ripple_id), "nearbyRipples": ripples_nearby}), 200
    
    # As ripples nearby is 5000m, we need to check if the distance is less than 150m
    ripples_within_150 = filter(lambda ripple: geodesic(user_location, 30 < tuple(ripple["center"]["coordinates"])).meters <= 150, ripples_nearby)
        
    if ripples_within_150 and len(ripples_within_150) > 0:
        print("NOTIFICATION: Ripple nearby within 150m, but not close enough to join")
        return jsonify({"message": "Ripple nearby within 150m, but not close enough to join", "nearbyRipples": ripples_nearby}), 200

    # Join ripple if within 30 meters
    for ripple in ripples_nearby:
        distance = geodesic(user_location, tuple(ripple["center"]["coordinates"])).meters
        if distance <= 30:
            ripples_collection.update_one(
                {"_id": ripple["_id"]},
                {"$addToSet": {"members": user_id}}
            )
            return jsonify({"message": "Joined ripple", "ripple_id": str(ripple["_id"]), "nearbyRipples": ripples_nearby }), 200

    # If no ripple joined or created
    return jsonify({"message": "No ripple joined or created", "nearbyRipples": ripples_nearby}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)

