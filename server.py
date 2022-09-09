"""Server for movie ratings app."""

import re
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def index():
    """View homepage."""
    logged_in = False
    if session['user_id']:
        logged_in = True

    return render_template('homepage.html', logged_in=logged_in)


@app.route('/movies')
def show_movies():
    """Show all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def show_movie_details(movie_id):
    """Shows details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    """Show all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users/<user_id>')
def show_user_details(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/users', methods=['POST'])
def create_user():
    """Create new user with info from create account form."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('''That email is associated with an existing user. 
              Try a different email.''')          
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user successfully created. You may log in now.')

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    """Process login form."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user.password == password:
        session['user_id'] = user.user_id
        flash(f'Logged in as {user.email}!')

    else:
        flash('Incorrect email or password. Try again.')

    return redirect('/')


@app.route('/new-rating', methods=['POST'])
def add_rating():
    """Add user rating to database."""

    title = request.form.get('title')
    score = int(request.form.get('score'))
    movie = crud.get_movie_by_title(title)
    user = crud.get_user_by_id(session['user_id'])


    if movie:
        new_rating = crud.create_rating(user, movie, score)
        db.session.add(new_rating)
        db.session.commit()
        flash('Rating successfully added!')
    else:
        flash('That movie is not in the database. Try a different title.')

    return redirect('/')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
