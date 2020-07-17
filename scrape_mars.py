from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mission_to_Mars

app = Flask(__name__)

# use pymongo to establish mongo connection
# mongo = PyMongo(app,uri = 'mongodb://localhost27017/mission_to_mars')
app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsData"
mongo = PyMongo(app)

# route to render template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    some_data = mongo.db.collection.find_one()

    return render_template("Mars_webpage.html", mars_info = some_data)

    


@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data = Mission_to_Mars.scrape()



    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)