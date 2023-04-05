
from sqlalchemy import Column, Integer, String, Boolean, Identity, ForeignKey
from sqlalchemy.orm import backref, relationship

from api.models.clients.clients_models import Clients
from api.repositories.db.mysql_db_context import AppDBConf


class Cameras(AppDBConf.BASE):
    __tablename__ = "Cameras"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    client_id = Column(Integer, ForeignKey("Clients.id"))
    device_name = Column(String)
    is_deleted = Column(Boolean)

    server_data = relationship(Clients, backref=backref("camera_owner", uselist=True, cascade="delete,all"))
