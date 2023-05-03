from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import timezone



jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

sched = BackgroundScheduler(daemon=True, jobstores=jobstores, timezone=timezone('America/Chicago'))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'InsertKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
sched.start()

from webserver import routes