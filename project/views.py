from flask import render_template, session, redirect, url_for
from project.forms import *
from project.models import *
from project.crud import Flask_crud

# Añade tus vistas aqui
def index():
    return render_template('index.html')