from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes