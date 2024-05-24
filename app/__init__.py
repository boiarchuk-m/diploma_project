from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_login import LoginManager

load_dotenv()

login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


login_manager.init_app(app)
login_manager.login_view = 'login'

from app.auth import auth
from app.user_management import user_management
from app.forecasting import forecasting
from app.reporting import reporting
from app.main import main

app.register_blueprint(auth)
app.register_blueprint(user_management)
app.register_blueprint(forecasting)
app.register_blueprint(main)
app.register_blueprint(reporting)
