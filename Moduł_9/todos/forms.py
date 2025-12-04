from flask_wtf import FlaskForm
from wtforms import FormField, IntegerField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class EmailPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code', [InputRequired])
    area_code    = IntegerField('Area Code/Exchange', [InputRequired()])
    number       = StringField('Number')

class ContactForm(FlaskForm):
    first_name   = StringField()
    last_name    = StringField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)

class TodoForm(FlaskForm):
    title       = StringField()
    description = StringField()
    done        = BooleanField()