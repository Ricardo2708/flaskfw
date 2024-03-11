from .views import *

# Create your url's here
def routing(app):
    app.add_url_rule('/', 'index', index)