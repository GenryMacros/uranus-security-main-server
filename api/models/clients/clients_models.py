
from sqlalchemy import Column, Integer, String, Boolean, Identity, ForeignKey, BINARY
from sqlalchemy.orm import backref, relationship

from api.repositories.db.mysql_db_context import AppDBConf


class Client(AppDBConf.BASE):
    __tablename__ = "Client"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    username = Column(String)
    is_deleted = Column(Boolean)


class ClientContact(AppDBConf.BASE):
    __tablename__ = "ClientContact"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    client_id = Column(Integer, ForeignKey("Client.id"))
    email = Column(String)
    phone = Column(String)
    telegram = Column(String)

    personal_data = relationship(Client, backref=backref("contact_owner", uselist=True, cascade="delete,all"))


class ClientPersonalData(AppDBConf.BASE):
    __tablename__ = "ClientPersonalData"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    client_id = Column(Integer, ForeignKey("Client.id"))
    user_first_name = Column(String)
    user_last_name = Column(String)

    client = relationship(Client, backref=backref("data_owner", uselist=True, cascade="delete,all"))


class ClientLocation(AppDBConf.BASE):
    __tablename__ = "ClientLocation"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    client_id = Column(Integer, ForeignKey("Client.id"))
    country = Column(String)
    city = Column(String)
    addr = Column(String)
    ind = Column(Integer)

    personal_data = relationship(Client, backref=backref("location_owner", uselist=True, cascade="delete,all"))


class ClientSecret(AppDBConf.BASE):
    __tablename__ = "ClientSecret"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    client_id = Column(Integer, ForeignKey("Client.id"))
    password_hash = Column(String)
    password_salt = Column(String)
    user_private = Column(BINARY)
    user_public = Column(BINARY)

    secret = relationship(Client, backref=backref("secret_owner", uselist=True, cascade="delete,all"))
