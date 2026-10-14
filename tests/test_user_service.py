from webapp.services import UserService
from webapp.schemas import UserCreate, UserUpdate


def test_create_user(mocker):
    repo = mocker.Mock()
    repo.create_user.return_value = {'id': 1, 'name': 'Alice', 'email': 'a@x.com'}
    us = UserService(repo)
    user = us.create_user(UserCreate(name='Alice', email='a@x.com'))
    repo.create_user.assert_called_once_with('Alice', 'a@x.com')
    assert user['id'] == 1


def test_get_user_not_found(mocker):
    repo = mocker.Mock()
    repo.get_user.return_value = None
    us = UserService(repo)
    assert us.get_user(999) is None


def test_update_user(mocker):
    repo = mocker.Mock()
    repo.update_user.return_value = {'id':1,'name':'Bob','email':'b@x.com'}
    us = UserService(repo)
    res = us.update_user(1, UserUpdate(name='Bob'))
    repo.update_user.assert_called_once_with(1, 'Bob', None)
    assert res['name']=='Bob'


def test_delete_user(mocker):
    repo = mocker.Mock()
    repo.delete_user.return_value = True
    us = UserService(repo)
    assert us.delete_user(1) is True
