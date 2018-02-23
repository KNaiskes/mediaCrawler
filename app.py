from flask import Flask, render_template,redirect,request,url_for,session
from db.database import *
from crawlFunctions import *

app = Flask(__name__)
app.secret_key = "keep_it_secret_keep_it_safe"

keyword = ""

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		if userExists(request.form["username"], request.form["password"]) == False:
				error = "Invalid login credentials"
		else:
			session["logged_in"] = True
			session["username"] = request.form["username"]
			return redirect(url_for("search"))
	return render_template("login.html", error = error)

@app.route("/search", methods=["GET", "POST"])
def search():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	global keyword
	keyword = request.form.get("keyword")
	print("Here is the keyword:", keyword)
	if request.method == "POST":
		return redirect(url_for("results"))

	return render_template("search.html")
				
@app.route("/results")
def results():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	fb = fbPlaces(keyword)
	tweets = getTweets(keyword)
	flickr = getFlickr(keyword)
	gplus = getGplus(keyword)
	reddit = getReddit(keyword)
	youtube = getYoutube(keyword)
	return render_template("results.html",fb=fb,tweets=tweets,flickr=flickr,gplus=gplus,reddit=reddit,youtube=youtube)

@app.route("/logout", methods=["GET", "POST"])
def logout():
	session.clear()
	return render_template("index.html")


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
