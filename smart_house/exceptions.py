# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>


class SensorValueNotAvailable(Exception):
    def __init__(self, sensor_name):
        message = ("Sensor value for sensor {sensor_name} not available.".
                        format(sensor_name=sensor_name))
        super(SensorValueNotAvailable, self).__init__(message)