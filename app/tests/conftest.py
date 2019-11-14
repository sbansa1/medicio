import pytest

from app import create_app
from app.blueprints.users.model import User
from app.config import TestingConfig
from app.extensions import db

@pytest.fixture(scope='module')
def new_user():
    """Tests the User Model class
    The Fixtures helps in using the User object for different Cases
    """
    data = {"id":1,"email": "saurabh.bnss0123@gmail.com", "name":"Saurabh", "password":"Helloworld"}
    user = User(**data)
    return user


@pytest.fixture(scope='module')
def test_client():
    """Creates a flask test client for functional tests"""

    #sets up the flask application
    flask_app = create_app(config_settings=TestingConfig)
    #initializes the test client
    testing_client = flask_app.test_client()

    #Establish and Creates an app context before running
    ctx = flask_app.app_context()
    #Pushes the app context to handle the GET and Post Request
    ctx.push()

    #This is where the real testing begins. Meaning the test client is avaliable to allow all the
    #integration tests cases with the client. Makes the test client available to integrate with the
    ##functional test

    yield testing_client

    #cleans up the test enviornment
    ctx.pop()

@pytest.fixture(scope='module')
def test_init_database():
    """Fixture that initializes the test Database"""

    #Creates the database and the database tables(helps in setting up)
    db.create_all()

    #creating User Instance to insert data in the Database.
    data1 = {"email": "saurabh.bnss0123@gmail.com", "name": "Saurabh", "password": "Helloworld"}
    data2 =  {"email": "meera.gadodia@gmail.com", "name": "Meera", "password": "HelloKitty"}

    user1 = User(**data1) #**kwargs strips data as per the key
    user2 = User(**data2)

    #Inserts the data in the database
    db.session.add(user1)
    db.session.add(user2)

    #Commits the data in the database for persistence.
    db.session.commit()

    #Makes the test database instance available to integrate with Pytest and executes the functional test.
    yield db


    #this is where the database instance is destroyed. In short takes care of tear down.
    db.drop_all()

