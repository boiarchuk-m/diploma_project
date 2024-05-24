from app import db
from app.user_management import user_management
from flask import render_template, request, flash, redirect, url_for

from app.models.user import User, admin_required
from app.user_management.forms import EditForm, AddForm

from flask_login import login_required


@user_management.route('/users')
def users():
    users = db.session.query(User).all()

    #users_all = [{'username': users.username, 'time': dates.time, 'datetime': dates.date_time} for dates in dates_time]
    return render_template('users.html', users = users)


@user_management.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = db.session.query(User).get_or_404(user_id)  
    print(user.is_admin)
    form = EditForm()

    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            user.change_password(form.password.data)
        if form.role.data == 'admin':
            user.is_admin = True
        else:
            user.is_admin = False
        db.session.commit()
        return redirect(url_for('user_management.users')) 

    form.username.data = user.username
    form.password.data = user.password_hash
    return render_template('edit_user.html', form=form)

    

@user_management.route('/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = AddForm()
    if form.validate_on_submit():
        new_user = User(form.username.data, form.password.data, form.role.data=='admin')
        db.session.add(new_user)
        db.session.commit()
    if request.method == 'POST':
        return redirect(url_for('user_management.users'))
    
    return render_template('create_user.html', form=form)
    

@user_management.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('user_management.users'))
    


