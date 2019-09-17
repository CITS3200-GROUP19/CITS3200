from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_admin import Admin
# from app.routes import MyModelView, NewView
# from app.models import User

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


# admin = Admin(server, template_mode='bootstrap3')
# admin.add_view(MyModelView(User, db.session))
# admin.add_view(NewView(name='back'))
