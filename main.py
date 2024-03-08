from flask import Flask
from config import Config
from project.urls import routing

# Configuracion De Flask
app = Flask(__name__,template_folder='project/templates',static_folder='project/static')
app.config.from_object(Config)

# Agregar rutas desde urls.py
routing(app)

# Inicio de la aplicacion 
if __name__ == '__main__':
    app.run()