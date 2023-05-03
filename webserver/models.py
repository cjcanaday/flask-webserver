from webserver import db, login_manager
from flask_login import UserMixin
from datetime import date

ACCESS = {
    'user': 0,
    'admin': 1
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    access = db.Column(db.Integer, nullable=False, default=0)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.access}')"

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level
    


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.String(7), nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    hidden = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Note('{self.week}', '{self.title}', '{self.hidden}')"
