from hashlib import sha1
from app import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=21),unique = True,nullable=False)
    email = db.Column(db.String(length=51),unique = True,nullable=False)
    password_hash = db.Column(db.String(length=128),nullable=False)
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = sha1(bytes(plain_text_password,"utf-8")).hexdigest()

    def check_password(self,passwd):
        return sha1(bytes(passwd,"utf-8")).hexdigest() == self.password_hash

    def get_id(self):
        return self.user_id
    #verified = db.Column(db.Boolean,nullable=False)

class Products(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(length=31),unique = True,nullable=False)
    item_photo = db.Column(db.String(length=39),unique=True,nullable=False)
    description = db.Column(db.String(length=1001),nullable=False)
    owner = db.Column(db.Integer(),db.ForeignKey('user.user_id'))