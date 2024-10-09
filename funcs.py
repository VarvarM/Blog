from sqlalchemy import insert, select, update, delete

from datetime import datetime
from database import sync_engine
from core.models.models import metadata, Blog_user, News, Comment


def create_tables():
    sync_engine.echo = False
    metadata.drop_all(sync_engine)
    metadata.create_all(sync_engine)
    sync_engine.echo = True


def insert_state(new_state):
    with sync_engine.connect() as conn:
        stmt = insert(News).values(
            [
                {"name": new_state[0], "text": new_state[1], "user": new_state[2],
                 "date": new_state[3]}
            ]
        )
        conn.execute(stmt)
        conn.commit()


def insert_comment(new_state):
    with sync_engine.connect() as conn:
        stmt = insert(Comment).values(
            [
                {"state_id": new_state[0], "text": new_state[1], "user": new_state[2],
                 "date": new_state[3]}
            ]
        )
        conn.execute(stmt)
        conn.commit()


def update_state(state):
    with sync_engine.connect() as conn:
        stmt = update(News).where(News.c.id == state[0]).values(name=state[1], text=state[2], date=state[-1])
        conn.execute(stmt)
        conn.commit()


def insert_basic():
    with sync_engine.connect() as conn:
        stmt = insert(News).values(
            [
                {"name": "Трейды в РЛ", "text": "В рокет лиге уберут трейд после 5 декабря", "user": "mikhail",
                 "date": datetime.now()},
                {"name": "Новый состав GENG", "text": "Firstkiller перешёл в GENG", "user": "mikhail",
                 "date": datetime.now()},
            ]
        )
        conn.execute(stmt)
        conn.commit()
    with sync_engine.connect() as conn:
        stmt = insert(Comment).values(
            [
                {"state_id": 1, "text": "WOW", "user": "kirill",
                 "date": datetime.now()},
                {"state_id": 1, "text": "bad:(", "user": "mikhail",
                 "date": datetime.now()},
                {"state_id": 2, "text": "вау", "user": "kirill",
                 "date": datetime.now()},
            ]
        )
        conn.execute(stmt)
        conn.commit()
    with sync_engine.connect() as conn:
        stmt = insert(Blog_user).values(
            [
                {"name": "mikhail", "hashed_password": "qwe"},
                {"name": "kirill", "hashed_password": "asd"},
            ]
        )
        conn.execute(stmt)
        conn.commit()


def select_all_states():
    with sync_engine.connect() as conn:
        stmt = select(News)
        return conn.execute(stmt)


def select_curr_state(state_id):
    with sync_engine.connect() as conn:
        stmt = select(News).where(News.c.id == state_id)
        return conn.execute(stmt)


def delete_curr_state(state_id, user):
    with sync_engine.connect() as conn:
        stmt = delete(News).where((News.c.id == state_id) & (News.c.user == user))
        res = conn.execute(stmt)
        conn.commit()
        return res


def select_all_comments(state_id):
    with sync_engine.connect() as conn:
        stmt = select(Comment).where(Comment.c.state_id == state_id)
        return conn.execute(stmt)


def delete_curr_comment(comment_id, user):
    with sync_engine.connect() as conn:
        stmt = delete(Comment).where((Comment.c.id == comment_id) & (Comment.c.user == user))
        res = conn.execute(stmt)
        conn.commit()
        return res


def select_curr_user(username, password):
    with sync_engine.connect() as conn:
        stmt = select(Blog_user).where((Blog_user.c.name == username) & (Blog_user.c.hashed_password == password))
        user = conn.execute(stmt).first()
        return user
        # return {"username": user[1], "hashed_password": user[2]}


# print(select_curr_user('mikhail', 'qwe'))
# print(type(select_curr_user('mikhail', 'qwe')))
# print(select_curr_user('mikhail', 'qweq'))
