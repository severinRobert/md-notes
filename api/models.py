from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, event
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


SMALLINT = 40
BIGINT = 500

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(SMALLINT), nullable=False, unique=True)
    email = Column(String(SMALLINT), unique=True)
    contact = Column(String(SMALLINT))
    password = Column(String(BIGINT), nullable=False)
    salt = Column(String(SMALLINT), nullable=False)
    states_id = Column(Integer, ForeignKey("states.id"))
    roles_id = Column(Integer, ForeignKey("roles.id"))

@event.listens_for(Users.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Users(username='admin', email='admin@outlook.com', password='d82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892', salt='admin', states_id=1, roles_id=3),
    ])
    session.commit()

@event.listens_for(Roles.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Roles(name='Visitor'),
        Roles(name='User'),
        Roles(name='Administrator')
    ])
    session.commit()
