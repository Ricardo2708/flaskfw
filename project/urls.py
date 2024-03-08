from .views import index

# añade tus urls de tus views al routing de flask
def routing(app):
    app.add_url_rule('/', 'index', index)