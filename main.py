from flask import Flask
from config import Config
from project.urls import routing
from project.models import models, manager
from flask_migrate import Migrate
from project.admin import init_admin

# Configuracion De Flask
app = Flask(__name__,template_folder='project/templates',static_folder='project/static')
app.config.from_object(Config)

# Agregar rutas desde urls.py
routing(app)

# Inicializa la DB desde models.py
models.init_app(app)
Migrate(app, models)

# Inicializa el panel de administración
with app.app_context():
    metadata = models.MetaData()
    metadata.reflect(bind=models.engine)
    migraciones_realizadas = 'alembic_version' in metadata.tables
    if migraciones_realizadas:
        registered_models = init_admin(app)

        @app.context_processor
        def inject_registered_models():
            return dict(registered_models=registered_models)


# Inicializa LoginManager desde models.py
with app.app_context():
    metadata = models.MetaData()
    metadata.reflect(bind=models.engine)
    migraciones_realizadas = 'alembic_version' in metadata.tables
    if migraciones_realizadas:
        manager.init_app(app)
        manager.login_view = 'login'

# Inicializa la aplicacion 
if __name__ == '__main__':
    app.run()