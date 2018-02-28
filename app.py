# import Dependencies
from flask import Flask, jsonify, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    listings = db.collection.find_one()
    return render_template('index.html', listings=listings)

@app.route("/scrape")
def scrape():    
    listings_data = scrape_mars.scrape()
    listings = db.listings
    listings.update({}, listings_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)