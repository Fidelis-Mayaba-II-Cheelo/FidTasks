from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from fidtasks import db, bcrypt
from fidtasks.users.forms import RegistrationForm, LoginForm, UpdateUsersForm, ResetRequestForm, ResetPasswordForm
from email.policy import default
from fidtasks.models import User
from fidtasks.users.utils import save_picture, send_reset_mail


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created successfully!", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.addTasks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) #Flasks built in way for logging a user in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('goals.createGoal'))
        else:
            flash(f"Login Unsuccessful! Please make sure you enter your correct credentials", 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/updateAccountInformation", methods=['GET', 'POST'])
@login_required
def updateUsers():
    form = UpdateUsersForm()
    if form.validate_on_submit():
        if form.user_image.data:
            picture_file = save_picture(form.user_image.data)
            current_user.user_image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your account has been updated!", 'success')
        return redirect(url_for('users.updateUsers'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.user_image)
    return render_template('update_users.html', title='Manage Account Information', form=form, image_file=image_file)

@users.route("/account", methods=['GET'])
@login_required
def account():
    user_image = url_for('static', filename='profile_pics/' + current_user.user_image)
    return render_template('account.html', title='My Account', user_image=user_image)




@users.route("/resetPassword", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/resetPassword/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)