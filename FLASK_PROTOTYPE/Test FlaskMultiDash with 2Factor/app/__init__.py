import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from flask_bootstrap import Bootstrap

from flask_admin import Admin
from app.routes import MyModelView, NewView, KeyGenView
from app.models import User, PatientTable, FactTable
from app.extensions import login_manager

from config import BaseConfig


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)
    bootstrap = Bootstrap(server)

    from app.dashapp1.layout import layout as layout1
    from app.dashapp1.callbacks import register_callbacks as register_callbacks1
    register_dashapp(server, 'Dashapp 1', 'dashboard1', layout1, register_callbacks1)

    from app.dashapp2.layout import layout as layout2
    from app.dashapp2.callbacks import register_callbacks as register_callbacks2
    register_dashapp(server, 'Dashapp 2', 'dashboard2', layout2, register_callbacks2)

    from app.dashapp3.layout import layout as layout3
    from app.dashapp3.callbacks import register_callbacks as register_callbacks3
    register_dashapp(server, 'Dashapp 3', 'dashboard3', layout3, register_callbacks3)

    register_extensions(server)
    register_blueprints(server)

    # login_manager = LoginManager()
    # login_manager.init_app(server)
    # login_manager.login_view = 'main.login'

    # admin = Admin(server, template_mode='bootstrap3')
    # admin.add_view(MyModelView(User, db.session))
    # admin.add_view(NewView(name='back'))

    return server


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport])
    # Push an application context so we can use Flask's 'current_app'
    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)
    _protect_dashviews(my_dashapp)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
        # if view_func.startswith(dashapp.routes_pathname_prefix):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import migrate

    with server.app_context():
        db.init_app(server)
        login_manager.init_app(server)
        login_manager.login_view = 'main.login'
        migrate.init_app(server, db)
        admin = Admin(server, template_mode='bootstrap3')
        admin.add_view(MyModelView(User, db.session))
        admin.add_view(MyModelView(PatientTable, db.session))
        admin.add_view(KeyGenView(name='Invite Key', endpoint='keygen'))
        admin.add_view(NewView(name='back'))


def register_blueprints(server):
    from app.routes import server_mod

    server.register_blueprint(server_mod)
