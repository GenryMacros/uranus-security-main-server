
from sqlalchemy import Column, Integer, String, Boolean, Identity, ForeignKey, Date
from sqlalchemy.orm import backref, relationship

from api.models.cameras.cameras_models import Cameras
from api.repositories.db.mysql_db_context import AppDBConf


class Invasion(AppDBConf.BASE):
    __tablename__ = "Invasion"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    camera_id = Column(Integer, ForeignKey("Cameras.id"))
    video_path = Column(String)
    created = Column(String)
    is_deleted = Column(Boolean)

    camera_data = relationship(Cameras, backref=backref("invasion_owner", uselist=True, cascade="delete,all"))


class Intruder(AppDBConf.BASE):
    __tablename__ = "Intruder"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column(String)


class InvasionIntruders(AppDBConf.BASE):
    __tablename__ = "InvasionIntruders"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    invasion_id = Column(Integer, ForeignKey("Invasion.id"))
    intruder_id = Column(Integer, ForeignKey("Intruder.id"))

    invasion_data = relationship(Invasion, backref=backref("invasion", uselist=True, cascade="delete,all"))
    intruder_data = relationship(Intruder, backref=backref("intruder", uselist=True, cascade="delete,all"))
