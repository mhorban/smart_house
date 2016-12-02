# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

import unittest

from smart_house import sql_model


class SensorsFixture(unittest.TestCase):
    def setUp(self):
        super(SensorsFixture, self).setUp()
        sql_model.connect_db()
        self.assertNotEqual(None, sql_model.session)
        db_session = sql_model.session()
        db_session.query(sql_model.Sensor).delete()
        db_session.query(sql_model.SensorValue).delete()
        db_session.commit()

    sensors = [
        {
            'name': 'humidity_1',
            'type_': 'fake-humidity',
            'room': 'small',
            'conn_str': 'http://192.168.10.10/value'
        }, {
            'name': 'temperature_1',
            'type_': 'fake-temp',
            'room': 'big',
            'conn_str': 'http://192.168.10.11/value'
        }
    ]

    def _add_sensors(self):
        db_session = sql_model.session()
        for sensor in self.sensors:
            db_session.add(sql_model.Sensor(**sensor))
            db_session.commit()

    sensor_values = [
        sql_model.SensorValue(
            sensor_name='humidity_1',
            value='50'),
        sql_model.SensorValue(
            sensor_name='temperature_1',
            value='25'),
        sql_model.SensorValue(
            sensor_name='humidity_1',
            value='55'),
        sql_model.SensorValue(
            sensor_name='temperature_1',
            value='24'),
    ]

    def _add_sensor_values(self):
        db_session = sql_model.session()
        for sensor_value in self.sensor_values:
            db_session.add(sensor_value)
            db_session.commit()