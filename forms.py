from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import InputRequired, Email, Length


class AddUserForm(FlaskForm):
    """ Form for adding new user accounts. """

    username = StringField("User Name", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LogInForm(FlaskForm):
    """ Form for logging in users. """

    username = StringField("User Name", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """ Form for adding and editing feedback. """

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextField("Content", validators=[InputRequired()])