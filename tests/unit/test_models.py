from src.app import Admin, Family_members_info

def test_new_admin():
    new_admin = Admin(username="name", password="password")
    assert new_admin.username == "name"
    assert new_admin.password == "password"

def test_new_family_member():
    new_member = Family_members_info(
        first_name="f_name", last_name="l_name",
        age=17 ,gender="male" ,phone_number=250784654598,
        phone_type="Redim 4 pro")
    assert new_member.first_name == "f_name"
    assert new_member.last_name == "l_name"
    assert new_member.age == 17
    assert new_member.gender == "male"
    assert new_member.phone_number == 250784654598
    assert new_member.phone_type == "Redim 4 pro"
