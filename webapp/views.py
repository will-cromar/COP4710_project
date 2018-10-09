from flask import render_template

from . import app, db
from .forms import LoginForm, SignUpForm


@app.route('/')
def index():
    return "hello"


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute("INSERT INTO Users VALUES (%s, %s)",
                  (form.username.data, form.password.data))
        warns = c.fetchwarnings()
        if not warns:
            db.commit()

        c.close()
        # TODO: Real confirmation
        return "Created %s" % (form.username.data)

    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        c = db.cursor(named_tuple=True)
        c.execute("SELECT * FROM Users WHERE username=%s;",
                  (form.username.data,))
        user = c.fetchone()
        if user and user.passwd == form.password.data:
            # TODO: Log user in
            return user.username

    return render_template('login.html', form=form)
