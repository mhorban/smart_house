import unittest

from smart_house import parser

class TestRuleParser(unittest.TestCase):
    def test_calculations(self):

        def test(s, expVal, get_sensor_value_func=lambda x: 1000):
            rule_parser = parser.RuleParser(get_sensor_value_func)
            val = rule_parser.compute(s)

            if val == expVal:
                print s, "=", val, "=>", rule_parser.exprStack
            else:
                print s + "!!!", val, "!=", expVal, "=>", rule_parser.exprStack
                assert False

        test("9", 9)
        test("-9", -9)
        test("--9", 9)
        test("9 + 3 + 6", 9 + 3 + 6)
        test("9 + 3 / 11", 9 + 3.0 / 11)
        test("(9 + 3)", (9 + 3))
        test("(9+3) / 11", (9 + 3.0) / 11)
        test("9 - 12 - 6", 9 - 12 - 6)
        test("9 - (12 - 6)", 9 - (12 - 6))
        test("2*3.14159", 2 * 3.14159)
        test("3.1415926535*3.1415926535 / 10", 3.1415926535 * 3.1415926535 / 10)
        test("sin(0)", 0)
        test("2 + 3.14159 * 1 + 3", 2 + 3.14159 * 1 + 3)
        test("2 < 4", True)
        test("2 > 4", False)

        test("2 >= 4", False)
        test("2 <= 4", True)
        test("NOT(2 < 4)", False)
        test("NOT(2 >= 4)", True)

        test("NOT(2 == 2) OR 2 <= 4", True)
        test("NOT(2 == 2) OR 2 <= 4 AND 2 == 4", False)
        test("(NOT(2 == 2) OR 2 <= 4 AND 2 == 4) OR 1 == 1", True)
        test("(NOT(2 == 2) OR 2 <= 4 AND 2 == 4) OR 5 * 5 < 30", True)
        test("((NOT(2 == 2) OR 2 <= 4 AND 2 == 4) OR 5 * 5 < 30) AND 1 == 0", False)

        test("NOT(2 == 2) OR GET_SENSOR_VAL:sensor_1 > 2", True)
        test("NOT(2 == 2) OR GET_SENSOR_VAL:sensor_1 < 2", False)
        test("NOT(2 == 2) AND GET_SENSOR_VAL:sensor_1 < 2 OR GET_SENSOR_VAL:sensor_1 == 1000", True)

        class UnknownSensorException(Exception):
            pass
        def get_sensor_val_handler(sensor_name):
            assert sensor_name == "sensor_1"
            raise UnknownSensorException()
        self.assertRaises(UnknownSensorException, test, "NOT(2 == 2) OR GET_SENSOR_VAL:sensor_1 > 2",
                          True, get_sensor_val_handler)