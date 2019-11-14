import pytest
from app.blueprints.users.model import User

@pytest.fixture(scope='module')
def new_user():
    """Tests the User Model class
    The Fixtures helps in using the User object for different Cases
    """
    data = {"user_id":1,"email": "saurabh.bnss0123@gmail.com", "name":"Saurabh", "password":"Helloworld"}
    user = User(**data)
    return user



def test_new_user(new_user):
    """Unit Test (Tests the User Model)"""

    assert new_user.email == 'saurabh.bnss0123@gmail.com'
    assert new_user.password != "Helloworld"
    assert new_user.name == "Saurabh"


def test_generate_decode_token(new_user):
    """Unit test for Generate Token"""

    token = new_user.generate_token(user_id=new_user.user_id)
    assert new_user.decode_token(token=token) == 1



def test_decrypt_password(new_user):
    """This Test Case tests the encryption and decryption of password"""

    password = new_user.decrypt_password(new_user.password)
    assert password == True