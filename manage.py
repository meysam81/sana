from flask_script import Manager, prompt_bool
from sana import db, app
from sana.models import User, Request
from datetime import datetime
import threading
import time

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    print("db created successfully")

@manager.command
def dropdb():
    if prompt_bool("Are you sure?"):
        db.drop_all()
        print("db dropped successfully")

@manager.command
def add_user():
    user = User('989197050256')
    user.firstname = 'Meysam'
    user.lastname = 'Azad'
    user.password = 'test'
    db.session.add(user)
    db.session.commit()
    print('user added successfully')

if __name__ == '__main__':
    manager.run()
