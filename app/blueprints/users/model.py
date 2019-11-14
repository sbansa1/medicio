from time import time

from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from app.config import Config
from app.extensions import login_manager


class User(db.Model, UserMixin):

    """User Model"""

    __tablename__ = "Users"

    user_id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column( db.String(100), nullable=False)
    email = db.Column( db.String(100), nullable=False, unique=True)
    password = db.Column( db.String(200), nullable=True)
    address_1 = db.Column( db.String(100))
    address_2 = db.Column( db.String(100))
    city = db.Column( db.String(100))
    region = db.Column( db.String(100))
    postal_code = db.Column(db.String(100))
    mob_phone = db.Column(db.String(100))


    def __init__(self,*args,**kwargs):

        super(User,self).__init__(**kwargs)
        self.password =  User.encrypt_password(kwargs.get('password', ""))


    @classmethod
    def encrypt_password(cls, password_plaintext=None):

        if password_plaintext:
            password = generate_password_hash(password_plaintext,method="SHA256", salt_length=8)
            return password
        else:
            return None


    def decrypt_password(self,password='', with_password=True):

        if with_password:
            check_password_hash(self.password,password)
        return True


    def generate_token(self,user_id, expires_in=600):

        payload = {'user_id':user_id,"exp": time()+ expires_in}

        try:
            token = jwt.encode(payload=payload,
                           key=Config.SECRET_KEY,
                           algorithm='HS256').decode('UTF-8')

        except Exception as e:
            return "{0}".format(e)

        return token

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token,key=Config.SECRET_KEY,algorithms='HS256')['user_id']

        except jwt.InvalidTokenError as e:
            return "{0}".format(e)

        except jwt.InvalidTokenError as e:
            return "{0}".format(e)

        return payload


    @login_manager.user_loader
    def load_user(self,user_id):
        """
        This callback is used to reload the user object from the user ID stored in the session
        :return: returns the user
        """
        return User.query.get(int(user_id))


    def check_user_identity(self,email):

        if email:
            user = User.query.filter(User.email==email).first()
            return user
        else:
            return {"Error Message": "User Not Found"}


    def to_json(self):
        """"""

    def __repr__(self):
        return '<User {}>'.format( self.email )


class Doctor(User):

    __tablename__ = 'doctors'

    registration_no = db.Column(db.String(100), nullable=False)
    year_of_registration = db.Column(db.Integer, nullable=False)
    state = db.Column("state_medical_council", db.String(100), nullable=False)


    def __init__(self, *args, **kwargs):

        super(Doctor,self).__init__(**kwargs)

    def __repr__(self):
        return '<Doctor {}>'.format(self.email)










