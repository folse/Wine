from flask import Flask
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.moment import Moment
from flask.ext.migrate import Migrate
from flask.ext.bootstrap import WebCDN
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, current_user

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

app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('//cdn.bootcss.com/jquery/2.1.4/')
app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN('//cdn.bootcss.com/bootstrap/3.3.5/')