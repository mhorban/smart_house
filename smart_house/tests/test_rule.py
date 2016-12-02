# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from smart_house.tests import fixtures
from smart_house import sql_model


class TestSqlModel(fixtures.SensorsFixture):

    CONDITION_STR_1 = "GET_SENSOR_VAL:humidity_1 >= 55 AND" \
                      " GET_SENSOR_VAL:temperature_1 < 25"
    CONDITION_STR_2 = "GET_SENSOR_VAL:humidity_1 >= 55 AND" \
                      " GET_SENSOR_VAL:temperature_1 < 25"
    CONDITION_STR_3 = "GET_SENSOR_VAL:humidity_1 >= 55 AND" \
                      " GET_SENSOR_VAL:temperature_1 < 25"
    CONDITION_STR_4 = "GET_SENSOR_VAL:humidity_1 >= 55 AND" \
                      " GET_SENSOR_VAL:temperature_1 < 25"
    def test_sensor_table(self):
        db_session = sql_model.session()
        self._add_sensors()
        self._add_sensor_values()