# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from smart_house.tests import fixtures
from smart_house import sql_model


class TestSqlModel(fixtures.SensorsFixture):

    def test_sensor_table(self):
        db_session = sql_model.session()
        self._add_sensors()
        self.assertEqual(db_session.query(sql_model.Sensor).count(), 2)
        #self.assertEqual(self.db_session.query(sql_model.Sensor).count(), 2)
        #return
        s1 = db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'humidity_1')
        self.assertEqual(s1.count(), 1)
        self.assertEqual(s1[0].room, 'small')
        s1.delete()
        db_session.commit()
        self.assertEqual(db_session.query(sql_model.Sensor).count(), 1)
        s2 = db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'temperature_1').one()
        s2.room = 'middle'
        db_session.commit()
        s2 = db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'temperature_1').one()
        self.assertEqual(s2.room, 'middle')
        s2 = db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.room == 'middle').update({'room': 'smart'})
        db_session.commit()
        s2 = db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'temperature_1').one()
        self.assertEqual(s2.room, 'smart')

    def test_sensor_value(self):
        db_session = sql_model.session()
        self._add_sensors()
        self._add_sensor_values()
        temp_values = db_session.query(sql_model.SensorValue).filter(
            sql_model.SensorValue.sensor_name == 'temperature_1').all()
        self.assertEqual(len(temp_values), 2)
        self.assertEqual(temp_values[0].value, "25")#"sensor_values.value)

