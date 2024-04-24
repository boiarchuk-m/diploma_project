from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    role =  SelectField('Role', validators=[DataRequired()], 
                          choices =[('user', 'user'), ('admin', 'admin')])
    submit = SubmitField('Register')

    def check_username(self, username):
        if User.query.filter_by(username=username).first():
            raise ValidationError("User already exists")
    

