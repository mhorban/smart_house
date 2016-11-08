# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from oslo_log import log as logging

from smart_house import sql_model


LOG = logging.getLogger(__name__)


def init_handler_devs():
    '''
    return dict with key DB name of sensor and value sensor's obj'
    '''
    db_session = sql_model.session()
    dev_map = {}
    for row_dev in db_session.query(sql_model.HandlerDev):
        dev = create_device(row_dev.type_, row_dev.name, row_dev.room, row_dev.conn_set_str)
        dev_map[row_dev.name] = dev
    return dev_map


def create_device(type_, *args, **kwargs):
    device = None
    if type_ == 'fake-device':
        device = FakeDevice(*args, **kwargs)
    return device


class HandlerDev(object):
    def __init__(self, name, room, get_str, *args, **kwargs):
        self.name = name
        self.room = room
        self.get_str = get_str

    def execute(self, action_type, action, priority):
        raise NotImplemented()


class FakeDevice(HandlerDev):
    def execute(self, action_type, action, priority):
        LOG.info("Fake Device handler")