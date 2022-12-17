from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LogInForm, FeedbackForm


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
    Process the registration form by adding a new user. Then redirect to user info page. """
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

        return redirect(f'/users/{user.username}', user=user)
    
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
            return redirect(f'/users/{user.username}')

        else:
            form.password.errors = ["* Username or Password is incorrect *"]

    return render_template('log-in.html', form=form)


@app.route('/users/<username>')
def show_secrets(username):
    """ Show information about the given user.
        Show all of the feedback that the user has given. """
    user = User.query.get_or_404(username)
    feedback = user.feedback
    return render_template('user-info.html', user=user, feedback=feedback)



@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """ Remove the user from the database and delete all of their feedback. 
    Clear any user information in the session and redirect to /. """
    
    if session.get('username') == username:
        user = User.query.get_or_404(username)

        db.session.delete(user)
        db.session.commit()
        session.pop("username")

    
    return redirect('/')



@app.route('/logout')
def log_out_user():
    """ Clear any information from the session and redirect to /. """
    session.pop("username")

    return redirect('/')


########## BEGIN FEEDBACK ROUTES ##########


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """ Display a form to add feedback. 
    Add a new piece of feedback and redirect to /users/<username> """
    form = FeedbackForm()

    if session.get('username'):
        
        true_user = session['username']

        # Check for correct username
        if true_user != username:
            return redirect(f'/users/{true_user}/feedback/add')

        # When user submits form add new feedback to db and redirect to user page
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title, content=content, username=true_user)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')


        # If user logged in and matches user in path show add feedback form.
        return render_template('add-feedback.html', form=form)
    
    # If user not logged in redirect to login form
    return redirect('/login')


@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def edit_feedback(feedback_id):
    """ Display a form to edit feedback.
    Update a specific piece of feedback and redirect to /users/<username>. """
    form = FeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)

    if session.get('username'):
        
        true_user = session['username']

        # Check for correct username
        if true_user != feedback.user.username:
            return redirect(f'/users/{feedback.user.username}')

        # When user submits form add new feedback to db and redirect to user page
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{feedback.user.username}')

        # If user logged in and matches user in path show edit feedback form.
        return render_template('edit-feedback.html', form=form, feedback=feedback)
    
    # If user not logged in redirect to login form
    return redirect('/login')


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """ Delete a specific piece of feedback and redirect to /users/<username>. """
    feedback = Feedback.query.get_or_404(feedback_id)

    if session.get('username'):
        
        true_user = session['username']

        # Check for correct username
        if true_user == feedback.user.username:
            db.session.delete(feedback)
            db.session.commit()
    
        return redirect(f'/users/{feedback.user.username}')

    # If user not logged in redirect to login form
    return redirect('/login')