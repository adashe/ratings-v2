"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """Shows homepage."""

    return render_template("homepage.html")


@app.route("/movies")
def show_movies():
    """Shows movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie_details(movie_id):
    """Shows movie details."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def show_users():
    """Shows users."""

    users = crud.get_users()

    return render_template("users.html", users=users)


@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """Shows user profiles."""

    user = crud.get_user_by_id(user_id)
    # user_ratings = crud.get_score_by_user_id(user_id)

    # return render_template("user_profile.html", user=user, user_ratings=user_ratings)
    return render_template("user_profile.html", user=user)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form['email']
    password = request.form["password"]
    
    if crud.get_user_by_email(email) is None:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has successfully been created. You may now log in.")

    else:
        flash("A user with that email already exists. Please enter a different email.")

    return redirect("/")


@app.route("/login", methods=['POST'])
def user_login():
    """Check the password and log in."""

    email = request.form['email']
    password = request.form["password"]

    user = crud.get_user_by_email(email)

    if user:
        if user.password == password:
            session['user_id']= user.user_id
            flash('Logged in!')
        else:
            flash('Wrong password.')

    else:
        flash("Please create an account.")

    return redirect('/')


@app.route("/rate-movie/<movie_id>", methods=['POST'])
def rating_movie(movie_id):
    """Allow to the user rate a movie."""

    user_id = session.get("user_id")

    if user_id is None:
        flash('Please log in.')
    
    else:
        score = request.form['score']
        movie = crud.get_movie_by_id(movie_id)
        user = crud.get_user_by_id(user_id)
        rating = crud.create_rating(user, movie, score)
        db.session.add(rating)
        db.session.commit()
        flash (f'Rating added! You gave {movie.title} a score of {score} stars.')

    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
