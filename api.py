from flask import Flask, jsonify
from mongodb import MongoConnection
import requests

# Configuration of Flask
app = Flask(__name__)

# Configuration of MongoDB
db_client = MongoConnection().client
db = db_client.Weather
collection = db.Time


# Function to get weather data from an API and store it in MongoDB
def get_and_save_data():
    api_key = "pvz9KfqGkplheifoqWYUwmccrBPPXfu4"
    url = f"http://dataservice.accuweather.com/locations/v1/129846?apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Store data in MongoDB
    collection.insert_one(data)


# Path to get the data store in MongoDB
@app.route("/obtener_datos", methods=["GET"])
def get_store():
    data = list(collection.find())
    return jsonify(data)

if __name__ == '__main__':
    get_and_save_data()
    app.run(host="0.0.0.0", port=5000, debug=True)
