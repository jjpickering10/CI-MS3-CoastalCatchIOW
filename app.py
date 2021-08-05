import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get('username').lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))

        register = {
            "username": request.form.get('username').lower(),
            "password": generate_password_hash(request.form.get('password'))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get('username').lower()
        flash('Registration Complete')
        return redirect(url_for("profile", username=session['user']))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get('username').lower()})

        if existing_user:
            if check_password_hash(
             existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                flash("Hello, {}".format(
                    request.form.get('username')))
                return redirect(url_for(
                    "profile", username=session['user']))

            else:
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

        else:
            flash('Incorrect Username and/or Password')
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session['user']})['username']

    created_reviews = list(mongo.db.reviews.find({"created_by": username}))
    print(created_reviews)

    if session['user']:
        return render_template(
            "profile.html", username=username, created_reviews=created_reviews)

    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    flash('You are logged out')
    session.pop('user')
    return redirect(url_for('login'))


@app.route("/get_locations")
def get_locations():
    locations = mongo.db.locations.find()
    return render_template("locations.html", locations=locations)


@app.route("/locations/<location_id>", methods=["GET", "POST"])
def locations(location_id):
    location = mongo.db.locations.find_one(
        {"_id": ObjectId(location_id)})

    comments = list(mongo.db.comments.find({"location_id": location_id}))
    reviews = list(mongo.db.reviews.find({"location_id": location_id}))

    if request.method == "POST":
        post = {
            "location_id": location_id,
            "location_name": location["location_name"],
            "review_title": request.form.get("review_title"),
            "review_description": request.form.get("review_description"),
            "created_by": session['user']
        }
        mongo.db.reviews.insert_one(post)
        flash('Post successful')
        return redirect(url_for('locations', location_id=post["location_id"]))
        # return redirect(url_for('get_locations'))

    return render_template(
        "posts.html", location=location, reviews=reviews, comments=comments)


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
    if request.method == "POST":
        updated_post = {
            "location_id": post["location_id"],
            "location_name": post["location_name"],
            "review_title": request.form.get("review_title"),
            "review_description": request.form.get("review_description"),
            "created_by": session['user']
        }
        mongo.db.reviews.update({"_id": ObjectId(post_id)}, updated_post)
        flash('Edit successful')
        return redirect(url_for('locations', location_id=post["location_id"]))

    # posts = mongo.db.reviews.find().sort("location_name", 1)
    return render_template("edit_post.html", post=post)


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
    mongo.db.reviews.remove({"_id": ObjectId(post_id)})
    flash("Post deleted")
    return redirect(url_for('locations', location_id=post["location_id"]))


@app.route("/add_comment/<post_id>", methods=["GET", "POST"])
def add_comment(post_id):
    posts = mongo.db.reviews.find_one(
        {"_id": ObjectId(post_id)})

    if request.method == "POST":
        post = {
            "post_id": posts["_id"],
            "location_id": posts["location_id"],
            "created_by": session['user'],
            "comments": request.form.get("comments")
        }
        mongo.db.comments.insert_one(post)
        flash('Comment successful')
        return redirect(url_for('locations', location_id=post["location_id"]))


@app.route("/edit_comment/<comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    comments = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    if request.method == "POST":
        updated_comment = {
            "post_id": comments["post_id"],
            "location_id": comments["location_id"],
            "created_by": session['user'],
            "comments": request.form.get("comments")
        }
        mongo.db.comments.update(
            {"_id": ObjectId(comment_id)}, updated_comment)
        flash('Edit successful')
        return redirect(
            url_for('locations', location_id=comments["location_id"]))

    return render_template("edit_comment.html", comments=comments)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
