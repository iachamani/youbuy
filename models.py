from hashlib import sha1
from app import db
class User(db.Model):
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
    #verified = db.Column(db.Boolean,nullable=False)