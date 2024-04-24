from app import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, username, password, is_admin=False):
        self.username=username
        self.password_hash=generate_password_hash(password)
        self.is_admin=is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def change_password(self, password):
        self.password_hash = generate_password_hash(password)




