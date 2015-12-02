from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_ = Column(String, nullable=False)
    room = Column(String, nullable=False)
    conn_str = Column(String)


class SensorValue(Base):
    __tablename__ = 'sensor_value'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    time_ = Column(DateTime, default=func.now())
    value = Column(String, nullable=False)


class HandlerDev(Base):
    __tablename__ = 'handler_dev'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_ = Column(String, nullable=False)
    room = Column(String, nullable=False)
    conn_str = Column(String)


class Rule(Base):
    __tablename__ = 'rule'
    id = Column(Integer, primary_key=True)
    cond = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    action = Column(String, nullable=False)


#engine = create_engine('sqlite:///orm_in_detail.sqlite')
engine = create_engine('mysql://smart:smart@localhost/smart_db')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)