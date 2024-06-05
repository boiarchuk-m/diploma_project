from app import db
from datetime import datetime, timezone
#import datetime


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    prob = db.Column(db.Float)
    date_time = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer)
    