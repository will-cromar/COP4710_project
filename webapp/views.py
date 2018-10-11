from flask import render_template, redirect
from flask_login import current_user, login_required, login_user

from . import app, db, models, login_manager
from .forms import CredentialsForm, LocationForm, UniversityForm


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
    form = CredentialsForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute("INSERT INTO Users(username, passwd) VALUES (%s, %s)",
                  (form.username.data, form.password.data))
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
    form = CredentialsForm()
    if form.validate_on_submit():
        user = models.get_user(form.username.data,)
        if user and user.passwd == form.password.data:
            # TODO: Log user in
            login_user(models.load_user(user.username))
            return redirect('/myname')

    return render_template('login.html', form=form)


@app.route('/locations', methods=["GET", "POST"])
def locations():
    form = LocationForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute(
            "INSERT INTO Locations(lname, latitude, longitude)"
            "VALUES (%s, %s, %s)",
            (form.name.data, form.latitude.data, form.longitude.data))
        warns = c.fetchwarnings()
        if not warns:
            db.commit()
        else:
            print(warns)

        return redirect("/")
    else:
        print(form.errors)

    return render_template('locations.html', form=form)


@app.route('/university/new', methods=["GET", "POST"])
def university_edit():
    form = UniversityForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute(
            "INSERT INTO Universities(uname, primarylid, pop, descr)"
            "VALUES (%s, %s, %s, %s)",
            (form.name.data, form.location_id.data, form.population.data,
             form.description.data))

        warns = c.fetchwarnings()
        if not warns:
            db.commit()
        else:
            print(warns)
    else:
        print(form.errors)

    return render_template('university/edit.html', form=form)
