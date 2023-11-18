from wtforms import Form, BooleanField, StringField, PasswordField, validators
import wtforms_json

wtforms_json.init()

class RegistrationForm(Form):
    username = StringField('username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField('username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired()])