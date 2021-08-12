import os
import datetime
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


def get_date():
    current_date = datetime.datetime.utcnow().replace(microsecond=0)
    return current_date


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
    if 'user' in session:
        username = mongo.db.users.find_one(
            {"username": session['user']})['username']
        user_details = mongo.db.users.find_one(
            {"username": session['user']}, {"password": 0})
        guru = mongo.db.users.find_one(
            {"username": session['user']})['is_guru']

        created_reviews = list(
            mongo.db.reviews.find({"created_by": username}))
        asked_questions = list(
            mongo.db.questions.find({"created_by": username}))

        if guru == "no":
            session['guru'] = "no"
        else:
            session['guru'] = "yes"

    # if session['user']:
        return render_template(
            "profile.html", username=username,
            created_reviews=created_reviews,
            asked_questions=asked_questions,
            user_details=user_details)

    return redirect(url_for('login'))


@app.route("/edit_profile/<username_id>", methods=["GET", "POST"])
def edit_profile(username_id):
    user_details = mongo.db.users.find_one(
        {"_id": ObjectId(username_id)}, {"password": 0})

    if request.method == "POST":
        if 'user_image' in request.files:
            user_image = request.files["user_image"]
            mongo.save_file(user_image.filename, user_image)

        updated_user = {
            "$set": {"user_description": request.form.get(
                "user_description"), "user_image": user_image.filename}
        }
        mongo.db.users.update_one({"_id": ObjectId(username_id)}, updated_user)
        flash('Edit successful')
        return redirect(url_for('profile', username=session['user']))

    if 'user' in session:
        return render_template(
            "edit_profile.html", user_details=user_details)

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
    return render_template("locations.html", locations=locations)


@app.route("/locations/<location_id>", methods=["GET", "POST"])
def locations(location_id):
    location = mongo.db.locations.find_one(
        {"_id": ObjectId(location_id)})

    comments = list(mongo.db.comments.find({"location_id": location_id}))
    reviews = list(mongo.db.reviews.find({"location_id": location_id}))

    if request.method == "POST":
        post_date = get_date()
        post = {
            "location_id": location_id,
            "location_name": location["location_name"],
            "review_title": request.form.get("review_title"),
            "review_description": request.form.get("review_description"),
            "created_by": session['user'],
            "date_created": post_date
        }
        mongo.db.reviews.insert_one(post)
        flash('Post successful')
        return redirect(url_for(
            'locations', location_id=post["location_id"]))
        # return redirect(url_for('get_locations'))

    return render_template(
        "posts.html", location=location, reviews=reviews, comments=comments)


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if 'user' in session:
        post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
        if request.method == "POST":
            updated_post = {
                "location_id": post["location_id"],
                "location_name": post["location_name"],
                "review_title": request.form.get("review_title"),
                "review_description": request.form.get("review_description"),
                "created_by": session['user'],
                "date_created": post["date_created"]
            }
            mongo.db.reviews.update(
                {"_id": ObjectId(post_id)}, updated_post)
            flash('Edit successful')
            return redirect(url_for(
                'locations', location_id=post["location_id"]))

        # posts = mongo.db.reviews.find().sort("location_name", 1)
        return render_template("edit_post.html", post=post)

    return redirect(url_for('login'))


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    if 'user' in session:
        post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
        mongo.db.reviews.remove({"_id": ObjectId(post_id)})
        flash("Post deleted")
        return redirect(url_for(
            'locations', location_id=post["location_id"]))

    return redirect(url_for('login'))


@app.route("/add_comment/<post_id>", methods=["GET", "POST"])
def add_comment(post_id):
    if 'user' in session:
        posts = mongo.db.reviews.find_one(
            {"_id": ObjectId(post_id)})
        comment_date = get_date()
        if request.method == "POST":
            post = {
                "post_id": posts["_id"],
                "location_id": posts["location_id"],
                "created_by": session['user'],
                "comments": request.form.get("comments"),
                "date_created": comment_date
            }
            mongo.db.comments.insert_one(post)
            flash('Comment successful')
            return redirect(url_for(
                'locations', location_id=post["location_id"]))

    return redirect(url_for('login'))


@app.route("/edit_comment/<comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    if 'user' in session:
        comments = mongo.db.comments.find_one(
            {"_id": ObjectId(comment_id)})
        if request.method == "POST":
            updated_comment = {
                "post_id": comments["post_id"],
                "location_id": comments["location_id"],
                "created_by": session['user'],
                "comments": request.form.get("comments"),
                "date_created": comments["date_created"]
            }
            mongo.db.comments.update(
                {"_id": ObjectId(comment_id)}, updated_comment)
            flash('Edit successful')
            return redirect(
                url_for('locations', location_id=comments["location_id"]))

        return render_template("edit_comment.html", comments=comments)

    return redirect(url_for('login'))


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    if 'user' in session:
        comments = mongo.db.comments.find_one(
            {"_id": ObjectId(comment_id)})
        mongo.db.comments.remove({"_id": ObjectId(comment_id)})
        flash("Comment deleted")
        return redirect(url_for(
            'locations', location_id=comments["location_id"]))

    return redirect(url_for('login'))


@app.route("/view_locations")
def view_locations():
    if 'user' in session and 'admin' in session:
        locations = list(mongo.db.locations.find().sort("location_name", 1))
        reviews = list(mongo.db.reviews.find().sort("review_title", 1))
        return render_template(
            "view_locations.html", locations=locations, reviews=reviews)

    return redirect(url_for('login'))


@app.route("/view_categories")
def view_categories():
    if 'user' in session and 'admin' in session:
        categories = list(mongo.db.categories.find().sort("category_name", 1))
        # reviews = list(mongo.db.reviews.find().sort("review_title", 1))
        return render_template(
            "view_categories.html", categories=categories)

    return redirect(url_for('login'))


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if 'user' in session and 'admin' in session:
        if request.method == "POST":

            category = {
                "category_name": request.form.get("category_name")
            }

            mongo.db.categories.insert_one(category)
            flash("New Category added")
            return redirect(url_for('view_categories'))

        return render_template("add_category.html")

    return redirect(url_for('login'))


@app.route("/edit_categories/<category_id>", methods=["GET", "POST"])
def edit_categories(category_id):
    if 'user' in session and 'admin' in session:
        categories = mongo.db.categories.find_one(
            {"_id": ObjectId(category_id)})
        if request.method == "POST":

            updated_category = {
                "category_name": request.form.get("category_name")
            }
            mongo.db.categories.update(
                {"_id": ObjectId(category_id)}, updated_category)
            flash('Edit successful')
            return redirect(url_for('view_categories'))

        return render_template("edit_category.html", categories=categories)

    return redirect(url_for('login'))


@app.route("/delete_categories/<category_id>")
def delete_categories(category_id):
    if 'user' in session and 'admin' in session:
        mongo.db.categories.remove({"_id": ObjectId(category_id)})
        flash("Category successfully deleted")
        return redirect(url_for('view_categories'))

    return redirect(url_for('login'))


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    if 'user' in session and 'admin' in session:
        if request.method == "POST":
            if 'location_image' in request.files:
                location_image = request.files["location_image"]
                mongo.save_file(location_image.filename, location_image)

            location = {
                "location_name": request.form.get("location_name"),
                "location_description": request.form.get(
                    "location_description"),
                "location_image": location_image.filename
            }

            mongo.db.locations.insert_one(location)
            flash("New Location added")
            return redirect(url_for('view_locations'))

        return render_template("add_location.html")

    return redirect(url_for('login'))


@app.route("/edit_locations/<location_id>", methods=["GET", "POST"])
def edit_locations(location_id):
    if 'user' in session and 'admin' in session:
        locations = mongo.db.locations.find_one(
            {"_id": ObjectId(location_id)})
        if request.method == "POST":
            if 'location_image' in request.files:
                location_image = request.files["location_image"]
                mongo.save_file(location_image.filename, location_image)

            updated_location = {
                "location_name": locations["location_name"],
                "location_description": request.form.get(
                    "location_description"),
                "location_image": location_image.filename
            }
            mongo.db.locations.update(
                {"_id": ObjectId(location_id)}, updated_location)
            flash('Edit successful')
            return redirect(url_for('view_locations'))

        return render_template("edit_location.html", locations=locations)

    return redirect(url_for('login'))


@app.route("/delete_locations/<location_id>")
def delete_locations(location_id):
    if 'user' in session and 'admin' in session:
        mongo.db.locations.remove({"_id": ObjectId(location_id)})
        flash("Location successfully deleted")
        return redirect(url_for('view_locations'))

    return redirect(url_for('login'))


@app.route("/ask_guru", methods=["GET", "POST"])
def ask_guru():
    questions = list(mongo.db.questions.find().sort("like_count", -1))
    liked_questions = questions[:3]
    categories = list(mongo.db.categories.find())
    replies = list(mongo.db.replies.find())
    likes = list(mongo.db.likes.find())
    users = list(mongo.db.users.find({"is_guru": "yes"}, {"password": 0}))
    if 'user' in session:
        liked_user = list(mongo.db.likes.find({"liked_user": session['user']}))
    else:
        liked_user = None
    # print(liked_user)
    if request.method == "POST":
        category_id = request.form.get("category_id")
        category_id_name = mongo.db.categories.find_one(
            {"_id": ObjectId(category_id)})

        question = {
            "category_id": request.form.get("category_id"),
            "category_name": category_id_name["category_name"],
            "question_title": request.form.get("question_title"),
            "question_description": request.form.get("question_description"),
            "created_by": session['user'],
            "like_count": 0
        }

        mongo.db.questions.insert_one(question)
        flash("New question added")
        return redirect(url_for('ask_guru'))
    return render_template(
        "ask_guru.html", questions=questions,
        replies=replies, users=users, likes=likes,
        categories=categories, liked_questions=liked_questions,
        liked_user=liked_user)


@app.route("/edit_question/<question_id>", methods=["GET", "POST"])
def edit_question(question_id):
    if 'user' in session:
        question = mongo.db.questions.find_one(
            {"_id": ObjectId(question_id)})
        if request.method == "POST":
            updated_question = {
                "category_id": question["category_id"],
                "category_name": question["category_name"],
                "question_title": request.form.get("question_title"),
                "question_description": request.form.get(
                    "question_description"),
                "created_by": session['user'],
                "like_count": question["like_count"]
            }
            mongo.db.questions.update(
                {"_id": ObjectId(question_id)}, updated_question)
            flash('Edit successful')
            return redirect(url_for('ask_guru'))

        # posts = mongo.db.reviews.find().sort("location_name", 1)
        return render_template("edit_question.html", question=question)

    return redirect(url_for('login'))


@app.route("/delete_question/<question_id>")
def delete_question(question_id):
    if 'user' in session:
        mongo.db.questions.remove({"_id": ObjectId(question_id)})
        flash("Question deleted")
        return redirect(url_for('ask_guru'))

    return redirect(url_for('login'))


@app.route("/like_question/<question_id>")
def like_question(question_id):
    if 'user' in session:
        like = list(mongo.db.likes.find(
            {"question_id": ObjectId(
                question_id), "liked_user": session['user']}))

        question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})

        if len(like) < 1:
            new_like = {
                "question_id": ObjectId(question_id),
                "liked_user": session['user']
            }
            updated_like = {
                "$set": {"like_count": question["like_count"] + 1}
            }
            mongo.db.likes.insert_one(new_like)
            mongo.db.questions.update_one(
                {"_id": ObjectId(question_id)}, updated_like)
            return redirect(url_for('ask_guru'))
        else:
            mongo.db.likes.remove({"question_id": ObjectId(
                question_id), "liked_user": session['user']})

            updated_like = {
                "$set": {"like_count": question["like_count"] - 1}
            }
            mongo.db.questions.update_one(
                {"_id": ObjectId(question_id)}, updated_like)

            return redirect(url_for('ask_guru'))
    flash("You must be logged in to like")
    return redirect(url_for("ask_guru"))


@app.route("/add_reply/<question_id>", methods=["GET", "POST"])
def add_reply(question_id):
    if 'user' in session and 'guru' in session:
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

    return redirect(url_for('login'))


@app.route("/edit_reply/<reply_id>", methods=["GET", "POST"])
def edit_reply(reply_id):
    if 'user' in session and 'guru' in session:
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

    return redirect(url_for('login'))


@app.route("/delete_reply/<reply_id>")
def delete_reply(reply_id):
    if 'user' in session and 'guru' in session:
        mongo.db.replies.remove({"_id": ObjectId(reply_id)})
        flash("Reply deleted")
        return redirect(url_for('ask_guru'))

    return redirect(url_for('login'))


@app.route("/update_user/<username_id>", methods=["GET", "POST"])
def update_user(username_id):
    if 'user' in session and 'admin' in session:
        if request.method == "POST":
            is_guru = "yes" if request.form.get("is_guru") else "no"
            updated_user = {
                "$set": {"is_guru": is_guru}
            }
            mongo.db.users.update_one(
                {"_id": ObjectId(username_id)}, updated_user)
            flash("Edit User successful")
            return redirect(url_for("profile", username=session['user']))

    return redirect(url_for('login'))


@app.route("/edit_users")
def edit_users():
    if 'user' in session and 'admin' in session:
        users = list(mongo.db.users.find({}, {"password": 0}))
        return render_template("edit_users.html", users=users)

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
