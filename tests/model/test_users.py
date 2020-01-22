from pytest import mark
from sqlalchemy import select

from status_monitor.model.tables import metadata
from status_monitor.model.users import Users


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
