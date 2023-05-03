from webserver import bcrypt, db
from webserver.models import User, Note

username = str(input("Enter Username:\n"))
plain_pass = str(input("Enter Password:\n"))
access = int(input("Enter Access:\n"))

hashed_password = bcrypt.generate_password_hash(plain_pass).decode('utf-8')

db.create_all()

user = User(username=username, password=hashed_password, access=access)
db.session.add(user)
db.session.commit()
