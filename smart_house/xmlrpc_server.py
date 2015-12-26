import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

# def is_even(n):
#     return n%2 == 0
# 
# server = SimpleXMLRPCServer(("localhost", 8000))
# print "Listening on port 8000..."
# server.register_function(is_even, "is_even")
# server.serve_forever()

def run_xml_rpc_server(rule_id_2_periodic_task_map):
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
    pass