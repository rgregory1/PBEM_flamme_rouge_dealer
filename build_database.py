import os
from myapp import db
from models import User

# Data to initialize database with
USERS = [
    {"username": "Doug", "password": "password", "account_type": 'organizer'},
    {"username": "Brockman", "password": "password", "account_type": 'member'},
    {"username": "rusti", "password": "password", "account_type": 'admin'},

]

# Delete database file if it exists currently
if os.path.exists("flamme_rouge.db"):
    os.remove("flamme_rouge.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in USERS:
    p = User(username=person.get("username"), password=person.get("password"), account_type=person.get("account_type"))
    db.session.add(p)

db.session.commit()