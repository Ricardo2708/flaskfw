from .models import *
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request, flash


class MicroBlogModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index.html'))
    
def register_admin_views(admin):
    models_to_register = []
    for model in models_to_register:
        admin.add_view(MicroBlogModelView(model, models.session))