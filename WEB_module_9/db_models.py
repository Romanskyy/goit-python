from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine


_DB = 'postgresql://postgres:1111@localhost:5432/postgres'
Base = declarative_base()
engine = create_engine(_DB)

all_dbs = engine.execute(
    'SELECT datname FROM pg_database;').scalars().fetchall()

if 'addressbook' not in all_dbs:
    connection = engine.connect()
    connection.execute('commit')
    connection.execute('CREATE database addressbook')
    connection.close()

_DB = 'postgresql://postgres:1111@localhost:5432/addressbook'
engine = create_engine(_DB, echo=False)
metadata = Base.metadata
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    contact_name = Column(String(250), nullable=False)
    contact_phones = relationship("Phone", back_populates="contact",
                                  cascade="all, delete, delete-orphan")


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    phone = Column(String(250), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship("Contact", back_populates="contact_phones")


Base.metadata.bind = engine
Base.metadata.create_all(engine)
