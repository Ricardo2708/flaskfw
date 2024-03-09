from flask import Flask
from config import Config
from project.urls import routing
from project.models import models
from flask_migrate import Migrate

# Configuracion De Flask
app = Flask(__name__,template_folder='project/templates',static_folder='project/static')
app.config.from_object(Config)

# Agregar rutas desde urls.py
routing(app)

# Inicializa la DB desde models.py
models.init_app(app)
Migrate(app, models)

# Inicializa la aplicacion 
if __name__ == '__main__':
    app.run()