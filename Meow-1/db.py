from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import bcrypt
import uuid

from models import Base, User, Post
from chal import add_fake_users


def init_db():
    engine = create_engine('sqlite:///neko.db')
    Base.metadata.create_all(engine)


def add_user(session, username, name, password, check_password):
    user = session.query(User).filter_by(username=username).first()
    if user:
        return (False, 'User already exists')

    if len(password) < 6:
        return (False, 'Password too short')

    if password != check_password:
        return (False, 'Passwords do not match')

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    instance = str(uuid.uuid4())

    add_fake_users(session, instance)

    new_user = User(username=username,
                    name=name,
                    password=hashed,
                    instance=instance)

    session.add(new_user)
    session.commit()

    return (True, 'User created')


def user_exists(session, username):
    user = session.query(User).filter_by(username=username).first()

    if not user:
        return (False, 'User does not exist')

    return (True, 'User exists')


def check_user(session, username, password):
    user = session.query(User).filter_by(username=username).first()

    if not user:
        return (False, 'User does not exist')

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return (True, user.name)
    else:
        return (False, 'Incorrect password')


def verified_user(session, username):
    user = session.query(User).filter_by(username=username).first()

    if not user:
        return (False, 'User does not exist')

    if not user.verified:
        return (False, 'User is not verified')

    return (True, 'User is verified')


def get_users(session, username):
    user = session.query(User).filter_by(username=username).first()

    if not user:
        return (False, 'User does not exist')

    users = session.query(User).filter_by(instance=user.instance).all()

    res = [{'username': u.username,
            'verified': u.verified,
            'name': u.name} for u in users if u.username != username]

    return (True, res)


def add_post(session, username, content, link, preview):
    if len(content) > 280:
        return (False, 'Post too long')

    user = session.query(User).filter_by(username=username).first()

    if not user:
        return (False, 'User does not exist')

    new_post = Post(posted_by=username,
                    instance=user.instance,
                    content=content,
                    link=link,
                    preview=preview)

    session.add(new_post)
    session.commit()

    return (True, 'Post created')


def get_post(session, post_id, instance):
    post = session.query(Post).filter_by(id=post_id,
                                         instance=instance).first()
    if not post:
        return (False, 'Post does not exist')

    poster = session.query(User).filter_by(username=post.posted_by).first()

    res = {'posted_by': post.posted_by, 'posted_name': poster.name,
           'content': post.content, 'preview': post.preview,
           'link': post.link, 'instance': post.instance,
           'id': post.id}

    return (True, res)


def add_follower(session, approver_username, follower_username):
    approver_user = session.query(User).filter_by(
        username=approver_username).first()
    follower_user = session.query(User).filter_by(
        username=follower_username).first()

    if not approver_user.private:
        return (False, "Approver account doesn't have private account")
    if not approver_user or not follower_user:
        return (False, 'User does not exist')

    if follower_user.username in approver_user.followers:
        return (True, 'User is already approved')

    temp_list = approver_user.followers.copy()
    temp_list.append(follower_user.username)
    # Re assigning updates PickleType for ORM
    approver_user.followers = temp_list
    session.commit()

    return (True, "Follower approved")


def get_posts(session, username):
    user = session.query(User).filter_by(username=username).first()

    if not user:
        return (False, 'User does not exist')

    posts = session.query(Post).filter_by(instance=user.instance).all()
    res = []

    for post in posts:
        poster = session.query(User).filter_by(username=post.posted_by).first()

        content = post.content
        preview = post.preview
        link = post.link

        if poster.private and poster.username != user.username:
            if username not in poster.followers:
                content = "<b>Private account</b><br>"\
                    "Only approved followers can view the post."
                preview, link = None, None

        res.append({'posted_by': post.posted_by, 'posted_name': poster.name,
                    'content': content, 'preview': preview,
                    'link': link, 'instance': post.instance,
                    'id': post.id})

    return (True, res[::-1])


def get_session():
    engine = create_engine('sqlite:///neko.db')
    if not (engine.dialect.has_table(engine, 'user') and
            engine.dialect.has_table(engine, 'post')):
        init_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    return DBSession()
