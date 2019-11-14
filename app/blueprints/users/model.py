from time import time

from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from app.config import Config
from app.extensions import login_manager
from app.utils.db_func import ResourceMixin


class Person(object):

        id = db.Column(db.Integer, primary_key=True, nullable=False)
        name = db.Column( db.String( 100), nullable=False)
        email = db.Column( db.String( 100 ), nullable=False, unique=True)
        password = db.Column( db.String(200), nullable=True)
        address_1 = db.Column(db.String(100 ))
        address_2 = db.Column( db.String(100))
        city = db.Column( db.String(100 ))
        region = db.Column( db.String(100))
        postal_code = db.Column( db.String(100))
        mob_phone = db.Column( db.String(100))


class Doctor(Person):

    __tablename__ = 'doctors'

    registration_no = db.Column(db.String(100), nullable=False)
    year_of_registration = db.Column(db.Integer, nullable=False)
    state = db.Column("state_medical_council", db.String(100), nullable=False)



    def __init__(self, *args, **kwargs):

        super(Doctor,self).__init__(*args,**kwargs)

    def __repr__(self):
        return '<Doctor {}>'.format(self.email)



class User(Person, db.Model, UserMixin,ResourceMixin):

    """User Model"""

    def __init__(self,*args,**kwargs):

        super(User,self).__init__(*args,**kwargs)
        self.password =  User.encrypt_password(kwargs.get('password', ""))

    @classmethod
    def check_user_identity(cls,identity):

        if identity:
            user = User.query.filter( User.email == identity ).first()
            return user
        else:
            return {"Error Message": "User Not Found"}


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


    def generate_token(self,id, expires_in=600):

        payload = {'id':id,"exp": time()+ expires_in}

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
            payload = jwt.decode(token,key=Config.SECRET_KEY,algorithms='HS256')['id']

        except jwt.InvalidTokenError as e:
            return "{0}".format(e)

        except jwt.InvalidTokenError as e:
            return "{0}".format(e)

        return payload


    @login_manager.user_loader
    def load_user(id):
        """
        This callback is used to reload the user object from the user ID stored in the session
        :return: returns the user
        """
        return User.query.get(int(id))



    def to_json(self):
        """"""




    def __repr__(self):
        return '<User {}>'.format( self.email )












