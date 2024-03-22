from .models import *
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request, flash
from flask_admin import BaseView, expose
from sqlalchemy import desc, inspect

def to_camel_case(text):
    return ''.join(word.title() for word in text.split('_'))

class MicroBlogModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
        

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))
    
    @expose('/', methods=['GET'])
    def index(self):
        path = request.path.strip('/').split('/')[1]
        class_model = globals().get(to_camel_case(path))
        primary_key_name = inspect(class_model).primary_key[0].name
        model = class_model.query.order_by(getattr(class_model, primary_key_name).desc()).all()
        return self.render('admin/private/dynamic/index.html', path = path, models = model )

def register_admin_views(admin):
    models_to_register = []
    for model in models_to_register:
        admin.add_view(MicroBlogModelView(model, models.session))
    return [model.__name__.lower() for model in models_to_register]
