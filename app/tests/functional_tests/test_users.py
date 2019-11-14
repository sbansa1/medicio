

def test_home_page(test_client):
    """Uses the fixture test_client to integrate with the functional tests"""

    response = test_client.get("/")

    assert response.status_code == 200
    assert b"someone@example" in response.data
    assert b"mailto:so" in response.data


def test_post_home_page(test_client):
    """When the post request is executed to fetch the login page"""

    response = test_client.post("/")
    assert response.status_code == 405
    assert b"someone@example" not in response.data

def test_valid_login_page(test_client):
    """Test case where the login page is loaded correctly"""

    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Username" or b"Email" in response.data
    assert b"password" in response.data

def test_valid_registration_page(test_client):
    """Test Case where the registration page is loaded correctly"""
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"Username" or b"Email" in response.data
    assert b"Password" or b"Password2" in response.data
    assert b"Address_1" and b"Address_2" in response.data

def test_user_registration(test_client,test_init_database):

    data = dict(name="saurabh",email="saurabh.bnss0123@gmail.com",password="Helloworld", password2="Helloworld",
                address_1="123..asasa", address_2="", city="indore", postal_code=452001,mob_phone=9826376555)

    response = test_client.post("/register",data=data)
    assert response.status_code ==200
    assert b"Register" in response.data
    assert b"submit" in response.data



def test_user_login_logout(test_client,test_init_database):
    """Requires the test_client and the test_database fixture"""

    data = dict(email="saurabh.bnss0123@gmail.com",password="Helloworld")
    response = test_client.post("/login",data=data)
    print(response.data)
    assert response.status_code == 200
    assert b"someone@example" in response.data
    assert b"mailto:so" in response.data
    assert b"Register" not in response.data
    assert b"logout" not in response.data

    response = test_client.get("/logout")
    assert response.status_code == 302







