from sqlalchemy import Column
from sqlalchemy import TIMESTAMP
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    forum = Column(String, nullable=False)
    href = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False)

    def __init__(self, title, forum, href, created_at):
        self.title = title
        self.forum = forum
        self.href = href
        self.created_at = created_at


class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    href = Column(String, nullable=False, unique=True)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    like = Column(Integer, nullable=False)
    comment_key = Column(String, nullable=False, unique=True)
    comment_created_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __int__(self, href, author, content, like, comment_key, comment_created_at, created_at):
        self.href = href
        self.author = author
        self.content = content
        self.like = like
        self.comment_key = comment_key
        self.comment_created_at = comment_created_at
        self.created_at = created_at


class Contents(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True)
    href = Column(String, nullable=False)
    content = Column(String, nullable=False)
    content_create_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __int__(self, href, content, content_create_at, created_at):
        self.href = href
        self.content = content
        self.content_create_at = content_create_at
        self.created_at = created_at
