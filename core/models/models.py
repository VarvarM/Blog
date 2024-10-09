from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
metadata = MetaData()

Blog_user = Table(
    'blog_user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True, nullable=False),
    Column('hashed_password', String, nullable=False)
)


News = Table(
    'news',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('text', String, nullable=False),
    Column('user', String, nullable=False),
    Column('date', TIMESTAMP, nullable=False),
)


Comment = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('state_id', Integer, ForeignKey(News.c.id), nullable=False),
    Column('text', String, nullable=False),
    Column('user', String, nullable=False),
    Column('date', TIMESTAMP, nullable=False),
)