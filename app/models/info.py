from app import db


class  Info(db.Model):
    __tablename__ = 'customer_info'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'email': self.email
        }
    
