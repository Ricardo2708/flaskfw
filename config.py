# IMPORTANTE 'cambia el DEBUG a false si desplegaras la aplicacion'
# define tu clave secreta para el envio de formularios
import os
directory = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    SECRET_KEY = 'clave'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(directory, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREFERRED_URL_SCHEME = 'http'
    APPLICATION_ROOT = '/'
    SERVER_NAME = 'localhost:5000'