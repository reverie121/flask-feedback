from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class AddUserForm(FlaskForm):
    """ Form for adding new user accounts. """

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LogInForm(FlaskForm):
    """ Form for logging in users. """

    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])