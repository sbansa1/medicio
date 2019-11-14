

def test_new_user(new_user):
    """Unit Test (Tests the User Model)"""

    assert new_user.email == 'saurabh.bnss0123@gmail.com'
    assert new_user.password != "Helloworld"
    assert new_user.name == "Saurabh"


def test_generate_decode_token(new_user):
    """Unit test for Generate Token"""

    token = new_user.generate_token(id=new_user.id)
    assert new_user.decode_token(token=token) == 1



def test_decrypt_password(new_user):
    """This Test Case tests the encryption and decryption of password"""

    password = new_user.decrypt_password(new_user.password)
    assert password == True