# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

import unittest

from smart_house import sql_model
 
 
class TestSqlModel(unittest.TestCase):
    def setUp(self):
        super(TestSqlModel, self).setUp()
        sql_model.connect_db()
        self.assertNotEqual(None, sql_model.session)
        self.db_session = sql_model.session()
        self.db_session.query(sql_model.Sensor).delete()
        self.db_session.commit()
         
 
    def test_Sensor(self):
        sensors = [sql_model.Sensor(
                    name='humidity_1',
                    type_='fake-humidity',
                    room='small',
                    conn_str='http://192.168.10.10/value'),
                   sql_model.Sensor(
                    name='temperature_1',
                    type_='fake-temp',
                    room='big',
                    conn_str='http://192.168.10.11/value'),
                   ]
        self.db_session.add(sensors[0])
        self.db_session.commit()
        self.db_session.add(sensors[1])
        self.db_session.commit()
        self.assertEqual(self.db_session.query(sql_model.Sensor).count(), 2)
        s1 = self.db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'humidity_1')
        self.assertEqual(s1.count(), 1)
        self.assertEqual(s1[0].room, 'small')
        s1.delete()
        self.db_session.commit()
        self.assertEqual(self.db_session.query(sql_model.Sensor).count(), 1)
        s2 = self.db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'temperature_1').one()
        s2.room = 'middle'
        self.db_session.commit()
        s2 = self.db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'temperature_1').one()
        self.assertEqual(s2.room, 'middle')
        s2 = self.db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.room == 'middle').update({'room': 'smart'})
        self.db_session.commit()
        s2 = self.db_session.query(sql_model.Sensor).filter(
                    sql_model.Sensor.name == 'temperature_1').one()
        self.assertEqual(s2.room, 'smart')