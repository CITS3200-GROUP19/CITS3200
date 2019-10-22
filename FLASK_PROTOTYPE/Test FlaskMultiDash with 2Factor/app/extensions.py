from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app as server
# from flask_admin import Admin
# from app.routes import MyModelView, NewView
# from app.models import User

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(
    server,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
# admin = Admin(server, template_mode='bootstrap3')
# admin.add_view(MyModelView(User, db.session))
# admin.add_view(NewView(name='back'))
