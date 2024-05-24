from app import  db
from flask import render_template, request, flash, redirect, url_for
from app.auth.forms import LoginForm, ChangePasswordForm
from app.auth import auth
from app.models.user import User

from flask_login import login_user, logout_user, current_user, login_required


@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    msg = None
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter_by(username=username).first()
        print(user)
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Wrong password. Please try again', 'error')
        else:
            flash('Unknown user', 'error')
           
    return render_template( 'login.html', form=form, msg=msg )


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/change_password')
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.change_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid current password.', 'danger')
    return render_template('change_password.html', form=form)

