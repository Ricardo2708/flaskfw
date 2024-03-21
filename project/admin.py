from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask import redirect, url_for, request, flash, session
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import *
from .register import register_admin_views
from datetime import datetime
from sqlalchemy import desc

class MicroBlogModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.index'))
    
    @expose('/', methods=['GET'])
    def index(self):
        if self.is_accessible():
            search_query = request.args.get('search_query')
            is_adminSearch = request.args.get('is_adminSearch')
            if search_query:
                if is_adminSearch:
                    username = current_user.name 
                    users = User.query.filter_by(is_admin=is_adminSearch).order_by(desc(User.id)).all()
                    return self.render('admin/private/users/user.html', 
                        username = username, 
                        active_link = 'user',
                        users = users
                    )
                nameUser = request.args.get('nameUser')
                username = current_user.name 
                users = User.query.filter_by(name=nameUser).order_by(desc(User.id)).all()
                return self.render('admin/private/users/user.html', 
                    username = username, 
                    active_link = 'user',
                    users = users
                )
            username = current_user.name 
            users = User.query.order_by(desc(User.id)).all()
            return self.render('admin/private/users/user.html', 
                username = username, 
                active_link = 'user',
                users = users
            )
        else:
            return redirect(url_for('login.index'))
    
    @expose('/edit', methods=['GET', 'POST'])
    def edit(self):
        if self.is_accessible():
            if request.method == 'GET':
                user_edit = request.args.get('user_edit')
                user = User.query.get(user_edit)
                return self.render('admin/private/users/edit.html', user = user)
            if request.method == 'POST':
                iduser = request.form['iduser']
                user = User.query.get(iduser)

                user.name = request.form['name'] 
                user.email = request.form['email'] 
                user.password_hash = generate_password_hash(request.form['password']) if len(request.form['password']) > 0 else user.password_hash
                user.is_admin = request.form.get('is_admin') == 'on'

                models.session.commit()
                flash(f'User Change', 'success')
                return redirect(url_for('user.index'))

            return self.render('admin/private/users/edit.html')
        else:
            return redirect(url_for('login.index'))
        
    @expose('/create', methods=['GET', 'POST']) 
    def create(self):
        if self.is_accessible():
            if request.method == 'POST':
                email = request.form['email']
                name = request.form['name']
                password = request.form['password']
                is_admin = True if request.form.get('is_admin') == 'on' else False
                if User.query.filter_by(name=name).first():
                    flash('User already exists')
                    pass
                else:
                    new_user = User(email = email, name=name, password_hash=password, is_admin=is_admin, created_at = datetime.utcnow())
                    models.session.add(new_user)
                    models.session.commit()
                    flash('User created successfully.')
                    return redirect(url_for('user.index'))
            return self.render('admin/private/users/create.html')
        else:
            return redirect(url_for('login.index'))

    @expose('/delete', methods=['GET', 'POST']) 
    def delete(self):
        if self.is_accessible():
            user_delete = request.args.get('user_delete')
            user = User.query.get(user_delete)
            models.session.delete(user)
            models.session.commit()
            flash(f'User {user.name} delete successfully.')  
            return redirect(url_for('user.index'))
        else:
            return redirect(url_for('login.index'))

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
                        flash(f'Welcome to the administration panel:  @{user.name}')
                        session['username'] = user.name
                        return redirect(url_for('admin.index'))
                    else:
                        flash('Restricted User | Verify your username and password')
                        pass
                else:
                    flash('Invalid Credentials | Verify your username and password')
                    pass
            else:
                flash('The User does not exist | Verify your username and password')
                pass
        return self.render('admin/public/login.html')

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
                flash('User already exists')
                pass
            else:
                new_user = User(email = email, name=name, password_hash=password, is_admin=True, created_at = datetime.utcnow())
                models.session.add(new_user)
                models.session.commit()
                flash('User created successfully. Please log in.')
                logout_user()
                return redirect(url_for('login.index'))
        flash('IMPORTANT: This page will only be available if there is NO administrator user')
        return self.render('admin/public/register.html')
     
class LogoutView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        flash('You have successfully logged out.')
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
            return self.render('admin/private/home.html')
        else:
            return redirect(url_for('login.index'))
    
def init_admin(app):
    admin = Admin(name='Admin', index_view=CustomAdminIndexView())
    admin.init_app(app)
    admin.add_view(LoginView(name='Login', endpoint='login'))
    admin.add_view(RegisterView(name='Register', endpoint='register'))
    admin.add_view(MicroBlogModelView(User, models.session))
    admin.add_view(LogoutView(name='Logout', endpoint='logout'))
    return register_admin_views(admin)
