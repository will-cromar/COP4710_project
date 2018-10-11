from flask import render_template, redirect
from flask_login import current_user, login_required, login_user

from . import app, db, models, login_manager
from .forms import LoginForm, SignUpForm


@login_manager.unauthorized_handler
def unauthorized():
    return "do better"


@app.route('/')
def index():
    return "hello"


@app.route('/myname')
@login_required
def secret():
    return current_user.username


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute("INSERT INTO Users VALUES (%s, %s, %s)",
                  (form.username.data, form.password.data, form.email.data))
        warns = c.fetchwarnings()
        if not warns:
            db.commit()
            login_user(models.load_user(form.username.data))

        c.close()
        # TODO: Real confirmation
        return redirect('/myname')

    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.get_user(form.username.data,)
        if user and user.passwd == form.password.data:
            # TODO: Log user in
            login_user(models.load_user(user.username))
            return redirect('/myname')

    return render_template('login.html', form=form)
