from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

models = SQLAlchemy()
manager = LoginManager()


@manager.user_loader
def load__user(Usuario_id):
    return User.query.get(Usuario_id)

# default model 'admin panel'
class User(models.Model, UserMixin):
    __tablename__ = 'user'
    id = models.Column(models.Integer, primary_key = True)
    email = models.Column(models.String(64), unique = True, index = True)
    name = models.Column(models.String(64), unique = True, index = True)
    password_hash = models.Column(models.String(128))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# Create your models here