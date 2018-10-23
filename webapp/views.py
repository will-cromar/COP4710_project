import base64

from flask import render_template, redirect, abort
from flask_login import current_user, login_required, login_user

from . import app, db, models, login_manager
from .forms import (CredentialsForm, LocationForm, UniversityForm,
                    StudentInfoForm, RSOForm, EventForm, PhotoForm)


@login_manager.unauthorized_handler
def unauthorized():
    return "do better"


@app.route('/')
def index():
    return render_template("home.html", title="Home")


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
        return redirect('/account/student')

    return render_template('form.html', action="/signup",
                           name="Sign up", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = CredentialsForm()
    if form.validate_on_submit():
        user = models.get_user(form.username.data,)
        if user and user.passwd == form.password.data:
            login_user(models.load_user(user.username))
            return redirect('/')

    return render_template('form.html', action="/login",
                           name="Log in", form=form)


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
@login_required
def university_edit():
    if not current_user.is_super_user():
        abort(403)

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

    return render_template('form.html', action="/university/new",
                           name="New University", form=form)


@app.route('/university/photo/add', methods=["GET", "POST"])
@login_required
def photo_add():
    if not current_user.is_super_user():
        abort(403)

    form = PhotoForm()
    form.univid.choices = models.get_universities()
    if form.validate_on_submit():
        f = form.photo.data

        c = db.cursor()
        c.execute(
            "INSERT INTO Photos(univid, b64, ftype)"
            "VALUES (%s, %s, %s)",
            (form.univid.data,
             base64.standard_b64encode(f.read()),
             f.mimetype))

        warns = c.fetchwarnings()
        if not warns:
            db.commit()
        else:
            print(warns)

    return render_template('form.html', action="/university/photo/add",
                           name="Add University Photo", fileform=True,
                           form=form)


@app.route('/account/student', methods=["GET", "POST"])
@login_required
def student_info():
    form = StudentInfoForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute(
            "INSERT INTO Students(username, univid, email)"
            "VALUES (%s, %s, %s)",
            (current_user.username, form.univid.data, form.email.data))

        warns = c.fetchwarnings()
        if not warns:
            db.commit()
        else:
            print(warns)
    else:
        print(form.errors)

    return render_template("form.html", action='/account/student',
                           name="Update Student Information", form=form)


@app.route('/rso/new', methods=["GET", "POST"])
@login_required
def rso_edit():
    form = RSOForm()
    if form.validate_on_submit():
        c = db.cursor()
        c.execute(
            "INSERT INTO RSOs(rsoname, approved)"
            "VALUES (%s, 0)",
            (form.name.data,))

        c.execute(
            "SELECT rid FROM RSOs WHERE rsoname = %s",
            (form.name.data,))

        rid = c.fetchone()[0]
        print(rid)

        c.execute(
                "INSERT INTO Admins(username, rid)"
                "VALUES (%s, %s)",
                (current_user.username, rid))

        c.execute(
                "INSERT INTO RSOMembers(username, rid)"
                "VALUES (%s, %s)",
                (current_user.username, rid))

        for u in (field for field in form if 'user' in str(field.label)):
            c.execute(
                "INSERT INTO RSOMembers(username, rid)"
                "VALUES (%s, %s)",
                (u.data, rid))

        warns = c.fetchwarnings()
        if not warns:
            db.commit()
        else:
            print(warns)
    else:
        print(form.errors)

    return render_template('form.html', action='/rso/new',
                           name="Register RSO", form=form)


@app.route('/rso/<rid>', methods=["GET", "POST"])
@login_required
def rso_view(rid):
    c = db.cursor(named_tuple=True)
    c.execute("SELECT * FROM ApprovedRSOs WHERE rid=%s;", (rid,))
    rso = c.fetchone()

    c.execute("SELECT * FROM RSOEvents WHERE rsorestriction=%s", (rid,))
    rows = c.fetchall()

    return render_template('rso/view.html', rows=rows, rso=rso)


@app.route('/rso/list', methods=["GET", "POST"])
def rso_list():
    c = db.cursor(named_tuple=True)
    c.execute("SELECT * FROM ApprovedRSOs;")
    return render_template('rso/list.html', rows=c.fetchall())


@app.route('/rso/<rid>/join', methods=["POST"])
@login_required
def rso_join(rid):
    if not current_user.is_student():
        abort(403)

    c = db.cursor()
    c.execute(
            "INSERT INTO RSOMembers(username, rid)"
            "VALUES (%s, %s)",
            (current_user.username, rid))

    warns = c.fetchwarnings()
    if not warns:
        db.commit()
    else:
        print(warns)

    return redirect("/rso/{}".format(rid))


@app.route('/rso/<rid>/approve', methods=["POST"])
@login_required
def rso_approve(rid):
    if not current_user.is_super_user():
        abort(403)

    c = db.cursor()
    c.execute(
            "UPDATE RSOs "
            "SET approved = 1 "
            "WHERE rid = %s",
            (rid,))

    warns = c.fetchwarnings()
    if not warns:
        db.commit()
    else:
        print(warns)

    return redirect("/rso/{}".format(rid))


@app.route('/event/new', methods=["GET", "POST"])
def event_edit():
    form = EventForm()
    form.restriction.choices = ([(0, "None"), (-1, "My University")] +
                                current_user.get_rsos())
    if form.validate_on_submit():
        if form.restriction.data == 0:
            urestriction, rsorestriction = None, None
        elif form.restriction.data == -1:
            urestriction = current_user.univid
            rsorestriction = None
        else:
            urestriction = None
            rsorestriction = form.restriction.data

        dtime = str(form.date.data) + " " + str(form.time.data)
        c = db.cursor()
        c.execute(
            "INSERT INTO Events(title, dtime, lid, cphone, cemail, "
            "urestriction, rsorestriction, approved) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (form.title.data, dtime, form.location_id.data,
                form.cphone.data, form.cemail.data, urestriction,
                rsorestriction, rsorestriction is not None))

        warns = c.fetchwarnings()
        if not warns:
            db.commit()
        else:
            print(warns)

    return render_template('form.html', action="/event/new",
                           name="Create event", form=form)


@app.route('/event/list', methods=["GET", "POST"])
def event_list():
    c = db.cursor(named_tuple=True)
    c.execute("SELECT * FROM ApprovedEvents;")
    return render_template('event/list.html', rows=c.fetchall())


@app.route('/event/<eid>', methods=["GET", "POST"])
@login_required
def event_view(eid):
    return render_template('event/view.html', eid=eid)


@app.route('/event/<eid>/approve', methods=["POST"])
@login_required
def event_approve(eid):
    if not current_user.is_super_user():
        abort(403)

    c = db.cursor()
    c.execute(
            "UPDATE Events "
            "SET approved = 1 "
            "WHERE eid = %s",
            (eid,))

    warns = c.fetchwarnings()
    if not warns:
        db.commit()
    else:
        print(warns)

    return redirect("/event/{}".format(eid))
