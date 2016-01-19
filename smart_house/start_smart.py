# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

import sys
import signal
import functools

from oslo_config import cfg
from oslo_log import log as logging

from smart_house import sql_model
from smart_house import handler
from smart_house import sensor
from smart_house import periodic_task
from smart_house import rule
from smart_house import xmlrpc_server


CONF = cfg.CONF

opts = [
    cfg.StrOpt('logger_name',
               default="smart_log",
               help='Name of the logger.'),
    ]

CONF.register_opts(opts)


def parse_args(argv, default_config_files=None):
    logging.register_options(CONF)
    CONF(argv[1:],
         project='smart_proj',
         version='smart_ver 0.0.1',
         default_config_files=default_config_files)


def main():
    parse_args(sys.argv)
    logging.setup(CONF, CONF.logger_name)
    log = logging.getLogger(__name__)
    log.info('Starting Smart')

    sql_model.connect_db()
    
    # initialize all devices from handler_dev table
    handler_devs = handler.init_handler_devs()
    
    # initialize all sensors from sensor table
    # 'active' sensors should start listen to incoming values
    # if many sensors share same listen port - singleton sensor should be used
    # this singleton should have mapping name_of_sensor TO sensor_name
    # where name_of_sensor come with value from sensor and sensor.id from DB
    #
    # all device for controll are sensors. for example 
    # controll button in web page is sensor too.
    sensors = sensor.init_sensors()
    
    # apply all rules, run periodic_task_loop
    task_loop = periodic_task.PeriodicTaskLoop()
    # Function apply_rules creates many PeriodicTasks using 
    #      - 'when' conditions
    #      - callbacks(callback, increment_tick_cb, finish_cb)
    # Callback must check sql_condition using table sensor_values and
    # if condition match DO action with device from handler_dev table
    # Each rule will produce 3 callbacks.
    # Callback functions will be generated with 
    #     - standart SET function and
    #     - arguments connected to SET func with functool.partial
    #       arguments will have condition str to choose device: device.id=XXX
    #       and VALUE which will be set with conn_set_str string
    # apply_db_rules returns mapping rule_id TO PeriodicTask
    rule_id_2_periodic_task_map = rule.apply_db_rules(
        task_loop, handler_devs, sensors)
    task_loop.start()
    
    # run xml-rpc server thread to accept WEB server request 
    # send map rule_id_2_periodic_task_map to controll existing rules
    # and add new if needed.
    # map rule_id_2_periodic_task_map must be synchronized with locker
    xmlrpc_loop = xmlrpc_server.run_xml_rpc_server(
        rule_id_2_periodic_task_map, handler_devs, sensors)
    
    task_loop.join()
    xmlrpc_loop.join()


if __name__ == "__main__":
    main()
