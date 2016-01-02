import unittest

from smart_house import sql_model
 
 
class TestSqlModel(unittest.TestCase):
    def setUp(self):
        super(TestSqlModel, self).setUp()
        sql_model.connect_db()
        self.assertNotEqual(None, sql_model.session)
        self.db_session = sql_model.session
        self.db_session().query(sql_model.Sensor).delete()
         
 
    def test_Sensor(self):
        sensor = sql_model.Sensor(
                    name='humidity_1',
                    type_='Humidity_XXX',
                    room='small',
                    conn_str='http://192.168.10.10/value')
        self.db_session().add(sensor)
         