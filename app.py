# import flask libraries
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars
import scraping

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

# Scrape and repeat all data until success is achieved
no_data = True
while no_data == True:
    mars_data = scrape_mars(startup=True)
    if mars_data['success'] == True:
        no_data = False
        
#create route that renders index.html template
@app.route("/")
def index():
    # find one document from our mongo db and return it
    listings = mongo.db.mars.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars = my_mars)

# Set our path to /scrape
@app.route("/scrape")
def scraper():
    # create a mars info database
    my_mars = mongo.db.mars
    my_mars_data = scraping.scrape_all()

    # update my_mars with the data that is being scraped
    my_mars.update({},{"$set":my_mars_data}, upsert = True)

    # return a message to our page so we know it was successful
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug = True)

browser.close()