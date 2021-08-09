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
            "password": generate_password_hash(request.form.get('password')),
            "user_description": "",
            "user_image": "",
            "is_admin": "no",
            "is_guru": "no"
        }
        mongo.db.users.insert_one(register)
        session["user"] = request.form.get('username').lower()
        session["admin"] = "no"
        session["guru"] = "no"
        flash('Registration Complete')
        return redirect(url_for("profile", username=session['user']))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get('username').lower()})

        if existing_user:
            is_admin = existing_user["is_admin"]
            is_guru = existing_user["is_guru"]
            if check_password_hash(
             existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                if is_admin == "no":
                    session['admin'] = "no"
                else:
                    session['admin'] = "yes"
                if is_guru == "no":
                    session['guru'] = "no"
                else:
                    session['guru'] = "yes"
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
    user_details = mongo.db.users.find_one(
        {"username": session['user']}, {"password": 0})
    guru = mongo.db.users.find_one(
        {"username": session['user']})['is_guru']

    created_reviews = list(mongo.db.reviews.find({"created_by": username}))
    asked_questions = list(mongo.db.questions.find({"created_by": username}))
    users = list(mongo.db.users.find({}, {"password": 0}))
    print(user_details)

    if guru == "no":
        session['guru'] = "no"
    else:
        session['guru'] = "yes"

    if session['user']:
        return render_template(
            "profile.html", username=username,
            created_reviews=created_reviews,
            asked_questions=asked_questions,
            users=users, user_details=user_details)

    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    flash('You are logged out')
    session.pop('user')
    session.pop('admin')
    session.pop('guru')
    return redirect(url_for('login'))


@app.route("/file/<filename>")
def file(filename):
    return mongo.send_file(filename)


@app.route("/get_locations")
def get_locations():
    locations = mongo.db.locations.find()
    print(session)
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


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    comments = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    mongo.db.comments.remove({"_id": ObjectId(comment_id)})
    flash("Comment deleted")
    return redirect(url_for('locations', location_id=comments["location_id"]))


@app.route("/view_locations")
def view_locations():
    locations = list(mongo.db.locations.find().sort("location_name", 1))
    reviews = list(mongo.db.reviews.find().sort("review_title", 1))
    return render_template(
        "view_locations.html", locations=locations, reviews=reviews)


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        if 'location_image' in request.files:
            location_image = request.files["location_image"]
            mongo.save_file(location_image.filename, location_image)

        location = {
            "location_name": request.form.get("location_name"),
            "location_description": request.form.get("location_description"),
            "location_image": location_image.filename
        }

        mongo.db.locations.insert_one(location)
        flash("New Location added")
        return redirect(url_for('view_locations'))

    return render_template("add_location.html")


@app.route("/edit_locations/<location_id>", methods=["GET", "POST"])
def edit_locations(location_id):
    locations = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    if request.method == "POST":
        if 'location_image' in request.files:
            location_image = request.files["location_image"]
            mongo.save_file(location_image.filename, location_image)

        updated_location = {
            "location_name": locations["location_name"],
            "location_description": request.form.get("location_description"),
            "location_image": location_image.filename
        }
        mongo.db.locations.update(
            {"_id": ObjectId(location_id)}, updated_location)
        flash('Edit successful')
        return redirect(url_for('view_locations'))

    return render_template("edit_location.html", locations=locations)


@app.route("/delete_locations/<location_id>")
def delete_locations(location_id):
    mongo.db.locations.remove({"_id": ObjectId(location_id)})
    flash("Location successfully deleted")
    return redirect(url_for('view_locations'))


@app.route("/ask_guru", methods=["GET", "POST"])
def ask_guru():
    questions = mongo.db.questions.find()
    replies = list(mongo.db.replies.find())
    users = list(mongo.db.users.find({"is_guru": "yes"}, {"password": 0}))
    print(users)
    if request.method == "POST":

        question = {
            "question_title": request.form.get("question_title"),
            "question_description": request.form.get("question_description"),
            "created_by": session['user']
        }

        mongo.db.questions.insert_one(question)
        flash("New question added")
        return redirect(url_for('ask_guru'))
    return render_template(
        "ask_guru.html", questions=questions, replies=replies, users=users)


@app.route("/edit_question/<question_id>", methods=["GET", "POST"])
def edit_question(question_id):
    question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    if request.method == "POST":
        updated_question = {
            "question_title": request.form.get("question_title"),
            "question_description": request.form.get("question_description"),
            "created_by": session['user']
        }
        mongo.db.question.update(
            {"_id": ObjectId(question_id)}, updated_question)
        flash('Edit successful')
        return redirect(url_for('ask_guru'))

    # posts = mongo.db.reviews.find().sort("location_name", 1)
    return render_template("edit_question.html", question=question)


@app.route("/delete_question/<question_id>")
def delete_question(question_id):
    mongo.db.questions.remove({"_id": ObjectId(question_id)})
    flash("Question deleted")
    return redirect(url_for('ask_guru'))


@app.route("/add_reply/<question_id>", methods=["GET", "POST"])
def add_reply(question_id):
    question = mongo.db.questions.find_one(
        {"_id": ObjectId(question_id)})

    if request.method == "POST":
        reply = {
            "question_id": question["_id"],
            "created_by": session['user'],
            "reply": request.form.get("reply")
        }
        mongo.db.replies.insert_one(reply)
        flash('Reply successful')
        return redirect(url_for('ask_guru'))


@app.route("/edit_reply/<reply_id>", methods=["GET", "POST"])
def edit_reply(reply_id):
    replies = mongo.db.replies.find_one({"_id": ObjectId(reply_id)})
    if request.method == "POST":
        updated_reply = {
            "question_id": replies["question_id"],
            "created_by": session['user'],
            "reply": request.form.get("reply")
        }
        mongo.db.replies.update(
            {"_id": ObjectId(reply_id)}, updated_reply)
        flash('Edit successful')
        return redirect(
            url_for('ask_guru'))

    return render_template("edit_reply.html", replies=replies)


@app.route("/delete_reply/<reply_id>")
def delete_reply(reply_id):
    mongo.db.replies.remove({"_id": ObjectId(reply_id)})
    flash("Reply deleted")
    return redirect(url_for('ask_guru'))


@app.route("/update_user/<username_id>", methods=["GET", "POST"])
def update_user(username_id):
    if request.method == "POST":
        is_guru = "yes" if request.form.get("is_guru") else "no"
        updated_user = {
            "$set": {"is_guru": is_guru}
        }
        mongo.db.users.update_one({"_id": ObjectId(username_id)}, updated_user)
        flash("Edit User successful")
        return redirect(url_for("profile", username=session['user']))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
