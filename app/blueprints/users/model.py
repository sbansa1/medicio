from collections import OrderedDict
from sqlalchemy import or_
from app.extensions import db
from flask_login import UserMixin
from app.extensions import login_manager
from app.utils.auth import AuthMixin
from app.utils.db_func import ResourceMixin

class Person(object):

    ROLE = OrderedDict([
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    ])

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False),
                     index=True, nullable=False, server_default='patient')

    name = db.Column( db.String( 100), nullable=False)
    email = db.Column( db.String( 100 ), nullable=False, unique=True)
    password = db.Column( db.String(200), nullable=True)
    address_1 = db.Column(db.String(100 ))
    address_2 = db.Column( db.String(100))
    city = db.Column( db.String(100 ))
    region = db.Column( db.String(100))
    postal_code = db.Column( db.String(100))
    mob_phone = db.Column( db.String(100))



class UserResource(Person, db.Model, UserMixin,ResourceMixin,AuthMixin):

    """User Model"""

    appointment_user = db.relationship('Appointment', backref='user_ap_status', lazy='dynamic')


    def __init__(self,*args,**kwargs):

        super(UserResource,self).__init__(*args,**kwargs)
        self.password =  UserResource.encrypt_password(kwargs.get('password', ""))

    @classmethod
    def check_user_identity(cls,identity):

        if identity:
            user = UserResource.query.filter(or_(UserResource.email == identity,UserResource.name == identity)).first()
            print(user)
            return (user)
        else:
            return {"Error Message": "User Not Found"}



    @login_manager.user_loader
    def load_user(id):
        """
        This callback is used to reload the user object from the user ID stored in the session
        :return: returns the user
        """
        return UserResource.query.get(int(id))

    def set_password(self,password):
      self.password = UserResource.encrypt_password(password_plaintext=password)

    def __repr__(self):
        return '<UserResource {}>'.format( self.email )











