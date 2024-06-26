from app import db


class Metrics(db.Model):
    __tablename__ = 'customer_metrics'

    id = db.Column(db.Integer, primary_key=True)
    tenure = db.Column(db.Float)
    #login_device = db.Column(db.String(10))
    login_device = db.Column(db.String(1))
    warehouse_to_home =db.Column(db.Float)
    #payment_mode = db.Column(db.String(25))
    payment_mode = db.Column(db.Integer)
    #gender = db.Column(db.String(6))
    gender = db.Column(db.String(1))
    hours_spend_on_app = db.Column(db.Float)
    number_of_devices = db.Column(db.Integer)
    #order_cat = db.Column(db.String(25))
    order_cat = db.Column(db.Integer)
    satisfaction_score = db.Column(db.Integer)
    orders_num = db.Column(db.Integer)
    complain = db.Column(db.Integer)
    coupons_used = db.Column(db.Integer)
    number_of_address = db.Column(db.Integer)
    cashback_amount = db.Column(db.Float)

    def serialize(self):
        return {
            'id': self.id,
            'tenure': self.tenure,
            'login_device' : self.login_device,
            'warehouse_to_home': self.warehouse_to_home,
            'payment_mode' : self.warehouse_to_home,
            'gender': self.gender,
            'hours_spend_on_app':self.hours_spend_on_app,
            'number_of_devices':self.number_of_devices,
            'order_cat':self.order_cat,
            'satisfaction_score': self.satisfaction_score,
            'orders_num': self.orders_num,
            'complain':self.complain,
            'coupons_used':self.coupons_used,
            'number_of_address':self.number_of_address,
            'cashback_amount': self.cashback_amount
        }


class Categories(db.Model):
     __tablename__ = 'categories'

     id = db.Column(db.Integer, primary_key=True)
     category = db.Column(db.String(25))


class Payment(db.Model):
     __tablename__ = 'payment'

     id = db.Column(db.Integer, primary_key=True)
     pay_type = db.Column(db.String(25))


class Metrics_old(db.Model):
    __tablename__ = 'customer_metrics_old'

    id = db.Column(db.Integer, primary_key=True)
    tenure = db.Column(db.Float)
    login_device = db.Column(db.String(10))
    warehouse_to_home =db.Column(db.Float)
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
