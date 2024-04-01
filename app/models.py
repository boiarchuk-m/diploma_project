from app import db


class Metrics(db.Model):
    __tablename__ = 'customer_metrics'

    id = db.Column(db.Integer, primary_key=True)
    tenure = db.Column(db.Float)
    login_device = db.Column(db.String(10))
    werehouse_to_home =db.Column(db.Float)
    payment_mode = db.Column(db.String(25))
    gender = db.Column(db.String(6))
    hours_spend_on_app = db.Column(db.Float)
    number_of_devices = db.Column(db.Integer)
    order_cat = db.Column(db.String(25))
    satisfaction_score = db.Column(db.Integer)
    orders = db.Column(db.Integer)
    complain = db.Column(db.Integer)
    coupons_used = db.Column(db.Integer)
    number_of_address = db.Column(db.Integer)
    cashback_amount = db.Column(db.Float)


class  Info(db.Model):
    __tablename__ = 'customer_info'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(50))

