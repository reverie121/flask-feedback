from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LogInForm


app = Flask(__name__)


app.config['SECRET_KEY'] = "do*not*tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

debug = DebugToolbarExtension(app)


########## BEGIN Routes ##########


@app.route('/')
def main():
    """ Redirect to /register. """
    return redirect('/register')


@app.route('/register', methods=['GET','POST'])
def new_user():
    """ Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name. 
    Process the registration form by adding a new user. Then redirect to /secret. """
    form = AddUserForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Returned hashed password
        user = User.register(username, password)

        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username  # keep logged in    

        return redirect(f"/users/{user.username}")
    
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def log_in_user():
    """ Show a form that when submitted will login a user. 
    This form should accept a username and a password. 
    Process the login form, ensuring the user is 
    authenticated and going to /secret if so. """
    form = LogInForm()

    if form.validate_on_submit():
        usr = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(usr, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.password.errors = ["Bad username/password"]

    return render_template('log-in.html', form=form)


@app.route('/users/<username>')
def show_secrets(username):
    """ Show information about the given user.
        Show all of the feedback that the user has given. """
    if session.get('username'):
        user = User.query.get_or_404(username)
        return render_template('user-info.html', user=user)

    return redirect('/')


@app.route('/logout')
def log_out_user():
    """ Clear any information from the session and redirect to /. """
    session.pop("username")

    return redirect('/')