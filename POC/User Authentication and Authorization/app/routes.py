# app/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, login_manager
from app.forms import LoginForm, RegistrationForm
from app.models import User

# Sample user data (replace this with a database)
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data in users:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            user_id = str(len(users) + 1)
            new_user = User(user_id, form.username.data, form.password.data)
            users[user_id] = new_user
            flash('Registration successful! Welcome, {}.'.format(new_user.username), 'success')
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form)
