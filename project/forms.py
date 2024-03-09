# define tus formularios
from .models import *
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField,BooleanField,RadioField,SelectField,TextAreaField,SubmitField,PasswordField
from wtforms import ValidationError