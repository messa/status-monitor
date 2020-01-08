from pytest import mark
from sqlalchemy import select

from status_monitor.model.tables import metadata
from status_monitor.model.users import Users


def test_generate_user_id():
    user_ids = [Users._generate_user_id() for i in range(100)]
    assert all(len(user_id) >= 8 for user_id in user_ids)
    assert len(set(user_ids)) == len(user_ids)


@mark.asyncio
async def test_user_oauth_login(loop, engine):
    users = Users(engine)
    user = await users.get_user_after_oauth(
        email='joe@example.com',
        name='Joe Smith',
        picture='https://example.com/picture.jpg',
        locale='en',
        google_id='123abcd')
    assert user.google_id == '123abcd'
    assert user.email == 'joe@example.com'
    assert user.name == 'Joe Smith'
    user2 = await users.get_user_after_oauth(
        email='joe2@example.com',
        name='Joe Smith 2',
        picture='https://example.com/picture2.jpg',
        locale='cs',
        google_id='123abcd')
    assert user2.id == user.id
    assert user2.email == 'joe2@example.com'
    assert user2.name == 'Joe Smith 2'




