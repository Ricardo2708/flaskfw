from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import *
from .register import register_admin_views

class MicroBlogModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index.html'))
    
class LoginView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user is not None:
                if check_password_hash(user.password_hash, password):
                    if user.is_admin == True:
                        login_user(user)
                        flash(f'Bienvenido al panel de administracion:  @{user.name}')
                        return redirect(url_for('admin.index'))
                    else:
                        flash('Usuario Restringido | Verifica tu usuario y contraseña')
                        pass
                else:
                    flash('Credenciales Invalidas | Verifica tu usuario y contraseña')
                    pass
            else:
                flash('El Usuario no existe  | Verifica tu usuario y contraseña')
                pass
        return self.render('admin/login.html')

    def is_accessible(self):
        return not current_user.is_authenticated
    
class RegisterView(BaseView):
    def is_accessible(self):
        user = User.query.filter_by(is_admin = True).count()
        if user == 0 : 
            return not current_user.is_authenticated
        else:
            if current_user.is_authenticated:
                return not current_user.is_authenticated
            else:
                return current_user.is_authenticated 

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        if request.method == 'POST':
            email = request.form['email']
            name = request.form['name']
            password = request.form['password']
            if User.query.filter_by(name=name).first():
                flash('El usuario ya existe')
                pass
            else:
                new_user = User(email = email, name=name, password_hash=password, is_admin=True)
                models.session.add(new_user)
                models.session.commit()
                flash('Usuario creado con éxito. Por favor, inicia sesión.')
                logout_user()
                return redirect(url_for('login.index'))
        flash('IMPORTANTE : Esta pagina solo estara disponible si NO hay un usuario administrador')
        return self.render('admin/register.html')
     
class LogoutView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        flash('Se ha cerrado sesion correctamente.')
        logout_user()
        return redirect(url_for('login.index'))
    
    def is_accessible(self):
        return current_user.is_authenticated
    
class CustomAdminIndexView(AdminIndexView):
    def __init__(self, **kwargs):
        super(CustomAdminIndexView, self).__init__(**kwargs)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.index'))
    
    @expose('/')
    def index(self):
        if self.is_accessible():
            # Renderizar una plantilla específica si el usuario tiene acceso
            return self.render('admin/home.html')
        else:
            # Si el usuario no tiene acceso, manejar la redirección o mostrar un mensaje de error
            return redirect(url_for('login.index'))
    
def init_admin(app):
    admin = Admin(name='Admin',template_mode='bootstrap3', index_view=CustomAdminIndexView())
    admin.init_app(app)
    admin.add_view(LoginView(name='Login', endpoint='login'))
    admin.add_view(RegisterView(name='Register', endpoint='register'))
    admin.add_view(MicroBlogModelView(User, models.session))
    register_admin_views(admin)
    admin.add_view(LogoutView(name='Logout', endpoint='logout'))
