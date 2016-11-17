# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey, func
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

from oslo_config import cfg

from smart_house import exceptions

db_opts = [
    cfg.StrOpt('db_connect_str',
               default='mysql://smart:smart@localhost/smart_db',
               help='Connection string used for sqlalchemy.create_engine.'),
    ]

cfg.CONF.register_opts(db_opts)

Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensor'
    TYPES = (
        ('fake-temp', 'Fake Temperature Sensor'),
        ('fake-humidity', 'Fake Humidity Sensor')
    )
    name = Column(String(128), primary_key=True)
    type_ = Column(ChoiceType(TYPES))
    room = Column(String(1024), nullable=False)
    conn_str = Column(String(1024))


class SensorValue(Base):
    __tablename__ = 'sensor_value'
    id = Column(Integer, primary_key=True)
    sensor_name = Column(String(128), ForeignKey('sensor.name',
                                                 ondelete='CASCADE'))
    time_ = Column(DateTime, default=func.now())
    value = Column(String(1024), nullable=False)

    @staticmethod
    def get_by_name(sensor_name):
        results = (session().
                   query(SensorValue).
                   filter_by(sensor_name=sensor_name).
                   order_by(sqlalchemy.desc(SensorValue.time_)).all())
        if not results.count():
            raise exceptions.SensorValueNotAvailable(sensor_name)
        return results[-1]


class HandlerDev(Base):
    __tablename__ = 'handler_dev'
    TYPES = (
        ('fake-device', 'Fake Device'),
    )
    name = Column(String(128), primary_key=True)
    type_ = Column(ChoiceType(TYPES))
    room = Column(String(1024), nullable=False)
    conn_set_str = Column(String(1024))


class Rule(Base):
    __tablename__ = 'rule'
    PRIORITIES = (
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    cond_when_start_time = Column(DateTime, default=func.now())
    cond_when_end_time = Column(DateTime)
    cond_when_tick_count = Column(Integer, default=-1)
    cond_when_tick_count_done = Column(Integer, default=0)
    cond_when_tick_period = Column(Integer, default=5)
    cond_sql = Column(String(16000), nullable=False)
    # one device can have many functions like on/off lamp or so
    # action_value can be used to increase lamp for 30%
    action_type = Column(String(256), nullable=False)
    action_value = Column(String(256), nullable=False)
    handler_dev_name = Column(String(128),
                              ForeignKey('handler_dev.name', ondelete='CASCADE'))
    priority = Column(ChoiceType(PRIORITIES), default='medium')
    done = Column(Boolean, unique=False, default=False)


session = None


def connect_db(db_connect_str=cfg.CONF.db_connect_str):
    engine = create_engine(db_connect_str)
    global session
    _session = sessionmaker(bind=engine)
    #session.configure(bind=engine)
    session = scoped_session(_session)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
