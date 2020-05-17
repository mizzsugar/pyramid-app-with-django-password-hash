import sample.libs.password


def test_check_password():
    password = 'password'
    hashed = sample.libs.password.make_password(password)
    assert sample.libs.password.check_password(password, hashed)


def test_invalid_password():
    password = 'password'
    wrong_password = 'wrong'
    hashed = sample.libs.password.make_password(password)
    assert not sample.libs.password.check_password(wrong_password, hashed)
