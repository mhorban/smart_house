# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from oslo_log import log as logging

from smart_house import sql_model


LOG = logging.getLogger(__name__)


def init_sensors():
    '''
    return dict with key DB name of sensor and value sensor's obj'
    '''
    db_session = sql_model.session()
    sensor_map = {}
    for row_sensor in db_session.query(sql_model.Sensor):
        sensor = create_sensor(row_sensor.type_, row_sensor.name, row_sensor.room, row_sensor.conn_str)
        sensor_map[row_sensor.name] = sensor
    return sensor_map


def create_sensor(type_, *args, **kwargs):
    sensor = None
    if type_ == 'fake-temp':
        sensor = FakeTemperatureSensor(*args, **kwargs)
    elif type_ == 'fake-humidity':
        sensor = FakeHumiditySensor(*args, **kwargs)
    return sensor


class Sensor(object):
    def __init__(self, name, room, get_str, *args, **kwargs):
        self.name = name
        self.room = room
        self.get_str = get_str

    def get_value(self):
        raise NotImplemented()

    # def start(self):
    #     # create PeriodicTask here
    #     raise NotImplemented()


class FakeTemperatureSensor(Sensor):
    def get_value(self):
        LOG.info("Fake Temperature Sensor")
        return 1


class FakeHumiditySensor(Sensor):
    def get_value(self):
        LOG.info("Fake Humidity Sensor")
        return 1