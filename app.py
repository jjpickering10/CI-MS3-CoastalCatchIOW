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
    """
    Returns current date without the microseconds
    """
    current_date = datetime.datetime.utcnow().replace(microsecond=0)
    return current_date


@app.route("/")
@app.route("/home")
def home():
    """
    Renders Landing Page
    """
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register Account.
    Checks for pre existing username.
    Redirects to profile page if successful,
    otherwise redirects to register page
    """
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
    """
    Login to account.
    Checks for existing username.
    Checks to match password.
    Redirects to profile page if successful,
    otherwise redirects to login page
    """
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
    """
    Profile page
    Checks for guru status.
    Finds user details and reviews, questions, fav posts
    of user.
    Redirects to login page if user not in session
    """
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
        fav_posts = list(
            mongo.db.favourites.find({"favourite_user": username}))

        if guru == "no":
            session['guru'] = "no"
        else:
            session['guru'] = "yes"

        return render_template(
            "profile.html", username=username,
            created_reviews=created_reviews,
            asked_questions=asked_questions,
            user_details=user_details, fav_posts=fav_posts)

    return redirect(url_for('login'))


@app.route("/edit_profile/<username_id>", methods=["GET", "POST"])
def edit_profile(username_id):
    """
    Edit profile page
    Updates user description and image
    Redirects to login page if user not in session
    """
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
    """
    Logs out user using pop() method
    Redirects to login
    """
    flash('You are logged out')
    session.pop('user')
    session.pop('admin')
    session.pop('guru')
    return redirect(url_for('login'))


@app.route("/file/<filename>")
def file(filename):
    """
    Returns file from mongoDB
    """
    return mongo.send_file(filename)


@app.route("/get_locations")
def get_locations():
    """
    Returns locations page with locations
    and ratings of each from MongoDB
    """
    locations = list(mongo.db.locations.find())
    ratings = list(mongo.db.ratings.find())
    return render_template(
        "locations.html", locations=locations, ratings=ratings)


@app.route("/search_locations", methods=["GET", "POST"])
def search_locations():
    """
    Search locations
    """
    if request.method == "POST":
        location_query = request.form.get('location_query')
        locations = list(mongo.db.locations.find(
            {"$text": {"$search": location_query}}))
        ratings = list(mongo.db.ratings.find())
        return render_template(
            "locations.html", locations=locations, ratings=ratings)

    return redirect(url_for('get_locations'))


@app.route("/locations/<location_id>", methods=["GET", "POST"])
def locations(location_id):
    """
    Returns individual location page,
    with comments, reviews, ratings connected to location ID.
    If user in session, returns their rating and whether
    or not they have favourited the post.
    Inserts post to location page
    """
    location = mongo.db.locations.find_one(
        {"_id": ObjectId(location_id)})

    comments = list(mongo.db.comments.find({"location_id": location_id}))
    reviews = list(mongo.db.reviews.find({"location_id": location_id}))
    ratings = list(mongo.db.ratings.find(
        {"location_id": ObjectId(location_id)}))
    if 'user' in session:
        rating = mongo.db.ratings.find_one({"location_id": ObjectId(
            location_id), "rating_user": session['user']})
        fav_user = list(mongo.db.favourites.find(
            {"favourite_user": session['user']}))
    else:
        rating = None
        fav_user = None

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

    return render_template(
        "posts.html", location=location,
        reviews=reviews, comments=comments,
        rating=rating, ratings=ratings, fav_user=fav_user)


@app.route("/search_posts/<location_id>", methods=["GET", "POST"])
def search_posts(location_id):
    """
    Search posts within individual location.
    Searches all posts with the search, then loops through
    to find matching location id and appends to new list
    """
    if request.method == "POST":
        location = mongo.db.locations.find_one(
            {"_id": ObjectId(location_id)})

        comments = list(mongo.db.comments.find({"location_id": location_id}))
        posts_query = request.form.get('posts_query')
        all_reviews = list(mongo.db.reviews.find(
            {"$text": {"$search": posts_query}}))
        reviews = []
        for review in all_reviews:
            if review['location_id'] == location_id:
                reviews.append(review)
        ratings = list(mongo.db.ratings.find(
            {"location_id": ObjectId(location_id)}))
        if 'user' in session:
            rating = mongo.db.ratings.find_one({"location_id": ObjectId(
                location_id), "rating_user": session['user']})
            fav_user = list(mongo.db.favourites.find(
                {"favourite_user": session['user']}))
        else:
            rating = None
            fav_user = None

        return render_template(
            "posts.html", location=location,
            reviews=reviews, comments=comments,
            rating=rating, ratings=ratings, fav_user=fav_user)

    return redirect(url_for('get_locations'))


@app.route("/view_post/<post_id>")
def view_post(post_id):
    """
    View individual post from location page
    in seperate page
    Searches if user has favourited the post
    If post doesnt exist, returns to locations page
    with message.
    """
    post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
    if post:
        comments = list(mongo.db.comments.find(
            {"location_id": post['location_id']}))
        if 'user' in session:
            fav_user = list(mongo.db.favourites.find(
                    {"favourite_user": session['user']}))
        else:
            fav_user = None
        return render_template(
            "view_post.html", post=post, comments=comments, fav_user=fav_user)
    flash("Post does not exist")
    return redirect(url_for('get_locations'))


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """
    Edit post if user is in session,
    otherwise redirects to login
    Updates post and returns to location page
    of the post
    """
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

        return render_template("edit_post.html", post=post)

    return redirect(url_for('login'))


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    """
    If user in session, deletes post and
    redirects to location page of the post.
    Otherwise redirect to login.
    """
    if 'user' in session:
        post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
        mongo.db.reviews.remove({"_id": ObjectId(post_id)})
        flash("Post deleted")
        return redirect(url_for(
            'locations', location_id=post["location_id"]))

    return redirect(url_for('login'))


@app.route("/add_comment/<post_id>", methods=["GET", "POST"])
def add_comment(post_id):
    """
    Posts comment for post if user in session,
    otherwise redirects to login
    """
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
    """
    Edit comment if user in session,
    otherwise redirect to login
    """
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
    """
    Delete comment if user in session,
    otherwise redirect to login
    """
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
    """
    Admin page for viewing locations.
    Returns all locations and reviews from
    database
    """
    if 'user' in session and 'admin' in session:
        locations = list(mongo.db.locations.find().sort("location_name", 1))
        reviews = list(mongo.db.reviews.find().sort("review_title", 1))
        return render_template(
            "view_locations.html", locations=locations, reviews=reviews)

    return redirect(url_for('login'))


@app.route("/view_categories")
def view_categories():
    """
    Admin page for viewing categories.
    Returns all categories from database
    """
    if 'user' in session and 'admin' in session:
        categories = list(mongo.db.categories.find().sort("category_name", 1))
        return render_template(
            "view_categories.html", categories=categories)

    return redirect(url_for('login'))


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    Admin page for adding category.
    Redirects to admin category page
    """
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
    """
    Admin page for editing categories.
    Updates category name in database
    """
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
    """
    Admin page for deleting categories.
    Redirects to admin category page.
    """
    if 'user' in session and 'admin' in session:
        mongo.db.categories.remove({"_id": ObjectId(category_id)})
        flash("Category successfully deleted")
        return redirect(url_for('view_categories'))

    return redirect(url_for('login'))


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    """
    Admin page for adding location.
    Inserts new location into database
    """
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
    """
    Admin page for editing location.
    Updates image and location description.
    Location name can't be updated.
    """
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
    """
    Admin page for deleting locations.
    Redirects to admin locations page
    """
    if 'user' in session and 'admin' in session:
        mongo.db.locations.remove({"_id": ObjectId(location_id)})
        flash("Location successfully deleted")
        return redirect(url_for('view_locations'))

    return redirect(url_for('login'))


@app.route("/ask_guru", methods=["GET", "POST"])
def ask_guru():
    """
    Returns ask guru page with all questions,
    categories, replies, likes and users.
    Searches for like in likes db collection.
    Searches top 3 most liked questions.
    Inserts new question into datebase
    """
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
    if request.method == "POST":
        category_id = request.form.get("category_id")
        category_id_name = mongo.db.categories.find_one(
            {"_id": ObjectId(category_id)})

        question = {
            "category_id": request.form.get("category_id"),
            "category_name": category_id_name["category_name"],
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
    """
    Edit page for user question if user in session,
    otherwise redirect to login.
    Updates db with edited question.
    """
    if 'user' in session:
        question = mongo.db.questions.find_one(
            {"_id": ObjectId(question_id)})
        if request.method == "POST":
            updated_question = {
                "category_id": question["category_id"],
                "category_name": question["category_name"],
                "question_description": request.form.get(
                    "question_description"),
                "created_by": session['user'],
                "like_count": question["like_count"]
            }
            mongo.db.questions.update(
                {"_id": ObjectId(question_id)}, updated_question)
            flash('Edit successful')
            return redirect(url_for('ask_guru'))

        return render_template("edit_question.html", question=question)

    return redirect(url_for('login'))


@app.route("/delete_question/<question_id>")
def delete_question(question_id):
    """
    Deletes user question if user in session.
    Redirects to ask guru page
    """
    if 'user' in session:
        mongo.db.questions.remove({"_id": ObjectId(question_id)})
        flash("Question deleted")
        return redirect(url_for('ask_guru'))

    return redirect(url_for('login'))


@app.route("/like_question/<question_id>")
def like_question(question_id):
    """
    If user in session, checks if user has liked question.
    If so, removes like, otherwise adds like.
    """
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
    """
    Adds reply to question if user is guru
    user.
    """
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
    """
    Edits reply if user is guru
    """
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
    """
    Deletes reply if user is guru
    """
    if 'user' in session and 'guru' in session:
        mongo.db.replies.remove({"_id": ObjectId(reply_id)})
        flash("Reply deleted")
        return redirect(url_for('ask_guru'))

    return redirect(url_for('login'))


@app.route("/update_user/<username_id>", methods=["GET", "POST"])
def update_user(username_id):
    """
    Updates user guru status for admin
    """
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
    """
    Admin page for viewing all users guru status
    """
    if 'user' in session and 'admin' in session:
        users = list(mongo.db.users.find({}, {"password": 0}))
        return render_template("edit_users.html", users=users)

    return redirect(url_for('login'))


@app.route("/rate_location/<location_id>", methods=['GET', "POST"])
def rate_location(location_id):
    """
    Adds rating 1-5 from user for location.
    If rating already exists, updates rating to
    new rating.
    """
    if 'user' in session:
        rating = list(mongo.db.ratings.find(
            {"location_id": ObjectId(
                location_id), "rating_user": session['user']}))

        if request.method == "POST":
            if len(rating) < 1:
                new_rating = {
                    "location_id": ObjectId(location_id),
                    "rating": int(request.form.get("rating_score")),
                    "rating_user": session['user']
                }
                mongo.db.ratings.insert_one(new_rating)
                return redirect(url_for('locations', location_id=location_id))
            else:
                new_rating = {
                    "$set": {"rating": int(request.form.get("rating_score"))}
                }
                mongo.db.ratings.update_one({"location_id": ObjectId(
                    location_id), "rating_user": session['user']}, new_rating)
                return redirect(url_for('locations', location_id=location_id))
    flash("You must be logged in to rate")
    return redirect(url_for('locations', location_id=location_id))


@app.route("/favourite_post/<post_id>")
def favourite_post(post_id):
    """
    Favourites post for user.
    If favourite already exists, removes
    favourite. Otherwise adds favourite
    """
    post = mongo.db.reviews.find_one({"_id": ObjectId(post_id)})
    if 'user' in session:
        favourite = list(mongo.db.favourites.find(
            {"post_id": ObjectId(
                post_id), "favourite_user": session['user']}))

        if len(favourite) < 1:
            new_fav = {
                "post_id": ObjectId(post_id),
                "post_title": post['review_title'],
                "location_name": post['location_name'],
                "favourite_user": session['user']
            }
            mongo.db.favourites.insert_one(new_fav)
            return redirect(url_for(
                'locations', location_id=post['location_id']))
        else:
            mongo.db.favourites.remove({"post_id": ObjectId(
                post_id), "favourite_user": session['user']})
            return redirect(url_for(
                'locations', location_id=post['location_id']))
    flash("You must be logged in to favourite a post")
    return redirect(url_for("locations", location_id=post['location_id']))


@app.route("/contact_us")
def contact_us():
    """
    Renders contact page
    """
    return render_template('contact_us.html')


@app.route("/apply_guru/")
def apply_guru():
    """
    Renders apply guru page for logged in
    users
    """
    if 'user' in session:
        username = mongo.db.users.find_one(
            {"username": session['user']})['username']
        return render_template('apply_guru.html', username=username)

    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(e):
    """
    Renders error page for 404
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    Renders error page for 500
    """
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
