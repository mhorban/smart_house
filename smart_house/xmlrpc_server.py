# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading

from oslo_config import cfg
from oslo_log import log as logging

from smart_house import manager

opts = [
    cfg.IntOpt('xml_rpc_server_port',
               default=8000,
               help='Port of XML-RPC server.'),
    ]

cfg.CONF.register_opts(opts)
LOG = logging.getLogger(__name__)

# def is_even(n):
#     return n%2 == 0
# 
# server = SimpleXMLRPCServer(("localhost", 8000))
# print "Listening on port 8000..."
# server.register_function(is_even, "is_even")
# server.serve_forever()

def run_xml_rpc_server(rule_id_2_periodic_task_map,
                       handler_devs,
                       sensors):
    '''
    # run xml-rpc server thread to accept WEB server request 
    # send map rule_id_2_periodic_task_map to controll existing rules
    # and add new if needed.
    # map rule_id_2_periodic_task_map must be synchronized with locker
    # Basic XML-RPC server rules are:
    # add_rule(action_str, **kwargs)
    #    kwargs are fields from Rule table
    # del_rule(id)
    # get_all_rules()
    # get_rule(id)
    # update_rule(id, **rule_kwargs)
    #     will stop PeriodicTask, update DB and apply_rule()
    '''
    LOG.info("Starting XML-RPC server on port %d ..." % 
             cfg.CONF.xml_rpc_server_port)
    server = SimpleXMLRPCServer(("localhost", cfg.CONF.xml_rpc_server_port),
                                allow_none=True)
    server.register_introspection_functions()
    api_manager = manager.Manager()
    for method in api_manager.public_methods:
        LOG.debug('Register XML-RPC method %s' % method)
        server.register_function(getattr(api_manager, method), method)
    #xmlrpc_loop = threading.Thread(target=
    server.serve_forever()#)
    #xmlrpc_loop.start()
    #return xmlrpc_loop