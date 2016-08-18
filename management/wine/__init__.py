from flask import Flask
from flask_mail import Mail
from flask_admin import Admin
from flask_moment import Moment
from flask_migrate import Migrate
from flask_bootstrap import WebCDN
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='ADMIN', template_mode='bootstrap3')
from .admin import *

from main import main
from auth import auth
from specialist import specialist

app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(specialist, url_prefix='/specialist')

# Maybe better for China
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('//cdn.bootcss.com/jquery/2.1.4/')
app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN('//cdn.bootcss.com/bootstrap/3.3.5/')