
from sqlalchemy import Column, Integer, String, Boolean, Identity, ForeignKey, BINARY
from sqlalchemy.orm import backref, relationship

from api.repositories.db.mysql_db_context import AppDBConf


class Clients(AppDBConf.BASE):
    __tablename__ = "Clients"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    email = Column(String)
    username = Column(String)
    is_deleted = Column(Boolean)
    is_confirmed = Column(Boolean)


class ClientsAdditionalContacts(AppDBConf.BASE):
    __tablename__ = "ClientsAdditionalContacts"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    client_id = Column(Integer, ForeignKey("Clients.id"))
    phone = Column(String)
    telegram = Column(String)

    personal_data = relationship(Clients, backref=backref("contact_owner", uselist=True, cascade="delete,all"))


class ClientsLocations(AppDBConf.BASE):
    __tablename__ = "ClientsLocations"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    client_id = Column(Integer, ForeignKey("Clients.id"))
    country = Column(String)
    city = Column(String)
    addr = Column(String)
    ind = Column(Integer)

    personal_data = relationship(Clients, backref=backref("location_owner", uselist=True, cascade="delete,all"))


class ClientsSecrets(AppDBConf.BASE):
    __tablename__ = "ClientsSecrets"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    client_id = Column(Integer, ForeignKey("Clients.id"))
    password_hash = Column(String)
    password_salt = Column(String)
    user_private = Column(String)
    user_public = Column(String)

    secret = relationship(Clients, backref=backref("secret_owner", uselist=True, cascade="delete,all"))


class ClientsServersData(AppDBConf.BASE):
    __tablename__ = "ClientsServersData"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    client_id = Column(Integer, ForeignKey("Clients.id"))
    ip = Column(String)
    port = Column(String)

    server_data = relationship(Clients, backref=backref("server_owner", uselist=True, cascade="delete,all"))
