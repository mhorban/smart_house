from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oslo_config import cfg

db_opts = [
    cfg.StrOpt('db_connect_str',
               default='mysql://smart:smart@localhost/smart_db',
               help='Connection string used for sqlalchemy.create_engine.'),
    ]

cfg.CONF.register_opts(db_opts)

Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensor'
    name = Column(String, primary_key=True)
    type_ = Column(String, nullable=False)
    room = Column(String, nullable=False)
    conn_str = Column(String)


class SensorValue(Base):
    __tablename__ = 'sensor_value'
    id = Column(Integer, primary_key=True)
    sensor_name = Column(Integer, ForeignKey('sensor.name'))
    time_ = Column(DateTime, default=func.now())
    value = Column(String, nullable=False)


class HandlerDev(Base):
    __tablename__ = 'handler_dev'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_ = Column(String, nullable=False)
    room = Column(String, nullable=False)
    conn_set_str = Column(String)


class Rule(Base):
    __tablename__ = 'rule'
    id = Column(Integer, primary_key=True)
    cond_when_start_time = Column(DateTime, default=func.now())
    cond_when_end_time = Column(DateTime)
    cond_when_tick_count = Column(Integer, default=-1)
    cond_when_tick_count_done = Column(Integer, default=0)
    cond_when_tick_period = Column(Integer, default=5)
    cond_sql = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    action_dev_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    priority = Column(Integer, default=3);


session = None


def connect_db():
    engine = create_engine(cfg.CONF.db_connect_str)
    global session
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
