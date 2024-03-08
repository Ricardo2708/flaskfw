from flask import render_template, session, redirect, url_for
from .forms import *

# Añade tus vistas aqui
def index():
    return render_template('index.html')