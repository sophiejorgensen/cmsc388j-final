from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
   return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    email = db.EmailField(unique=True, required=True)
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Review(db.Document):
    commenter = db.ReferenceField(User)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    poke_name = db.StringField(required=True, min_length=1, max_length=50)

