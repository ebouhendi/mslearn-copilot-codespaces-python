from webapp.services import TokenService


def test_generate_length(mocker):
    # make os.urandom predictable
    mocker.patch('webapp.services.os.urandom', return_value=b"\x00" * 64)
    ts = TokenService()
    token = ts.generate(10)
    assert isinstance(token, str)
    assert len(token) == 10


def test_generate_default_length(mocker):
    mocker.patch('webapp.services.os.urandom', return_value=b"\x01" * 64)
    ts = TokenService()
    token = ts.generate(None)
    assert isinstance(token, str)
    assert len(token) == 20
