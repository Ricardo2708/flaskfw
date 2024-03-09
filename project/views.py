from flask import render_template, session, redirect, url_for, flash, request
from project.forms import *
from project.models import *
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# Añade tus vistas aqui
def index():
    return render_template('index.html')