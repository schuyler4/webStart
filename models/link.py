from sqlalchemy import Integer, String, Column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


engine = create_engine('sqlite:///users.db', echo=True)
Db_session = sessionmaker(bind=engine)
db_session = Db_session()


class Link(Base):
    __tablename__="Link"
    id = Column('link_id', Integer, primary_key=True)
    link = Column(String)
    description = Column(String)
    views = Column(Integer)
    owner = Column(String(100))

    def __init__(self, link, description, views, owner):
        self.link = link
        self.description = description
        self.views = views
        self.owner = owner


class User(Base):
    __tablename__="User"
    id = Column('user_id', Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


Base.metadata.create_all(engine)


