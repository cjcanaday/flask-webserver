
from flask import render_template, flash, url_for, redirect, request
from webserver import app, db, bcrypt, sched
from webserver.models import User, Note
from webserver.forms import LoginForm, NoteForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import asc, select, desc
from datetime import date


def unhide(identifier):
    print("unhiding")
    note = Note.query.filter_by(week=identifier).first()
    print(note)
    note.hidden = False
    db.session.add(note)
    db.session.commit()


@app.route("/")
@app.route("/home")
@login_required
def home():
    notes = Note.query.filter_by(hidden=False).order_by(Note.week.desc())
    return render_template('home.html', note=notes.first(), amount=len(notes.all()))

@app.route("/previous_notes")
@login_required
def previous_notes():
    notes = Note.query.filter_by(hidden=False).order_by(Note.week.asc())
    # Remove final (most recent) note because already shown
    previous_notes = notes[:-1]
    return render_template("previous_notes.html", notes=previous_notes)

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.  Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = NoteForm()
    if not current_user.is_admin():
        return redirect(url_for('login'))
    if request.method == "POST" and form.validate_on_submit():
        
        if form.upload_date.data != 'now':
            month, day, year = form.upload_date.data.split("/")
            dateobj = date(year=2000+int(year), month=int(month), day=int(day))
            
        note = Note(title=form.title.data, week=form.week.data, content=form.content.data)

        db.session.add(note)
        db.session.commit()

        unique_id = f"Week-{note.week}"
        if form.upload_date.data == 'now':
            unhide(note.week)
        else:
            sched.add_job(unhide, 'date', run_date=dateobj, args=[note.week], id=unique_id, misfire_grace_time=None, name=unique_id)

        return redirect(url_for('add'))
    return render_template('add.html', form=form)

