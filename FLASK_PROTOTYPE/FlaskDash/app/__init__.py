import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required, LoginManager
from flask_bootstrap import Bootstrap

from flask_admin import Admin
from app.routes import MyModelView, NewView
from app.models import User, PatientTable, FactTable
from app.extensions import db, login_manager

from config import BaseConfig

def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)
    bootstrap = Bootstrap(server)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    login_manager.init_app(server)
    login_manager.login_view = 'main.login'

    admin = Admin(server, template_mode='bootstrap3')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(PatientTable, db.session))
    admin.add_view(NewView(name='back'))

    return server


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_dashapps(app):
    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp1 = dash.Dash(__name__,
                         server=app,
                         routes_pathname_prefix='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport])
                         #,data = FactTable.query.all())

    with app.app_context():
        dashapp1.title = 'Dashapp 1'
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    _protect_dashviews(dashapp1)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith('/dashboard'):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login_manager
    from app.extensions import migrate

    db.init_app(server)
    login_manager.init_app(server)
    login_manager.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.routes import server_mod

    server.register_blueprint(server_mod)
