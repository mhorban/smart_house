# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from oslo_log import log as logging

LOG = logging.getLogger(__name__)

class Manager(object):
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
    public_methods = ['add_rule',
                      'del_rule',
                      'update_rule',
                      'get_rule',
                      'get_all_rules',
                      'exit']

    def add_rule(self):
        LOG.info("add_rule")
        raise NotImplementedError()
    
    def del_rule(self):
        LOG.info("add_rule")
        raise NotImplementedError()
        
    def update_rule(self):
        '''
        will stop PeriodicTask, update DB and apply_rule()
        '''
        LOG.info("update_rule")
        raise NotImplementedError()
        
    def get_rule(self):
        LOG.info("get_rule")
        raise NotImplementedError()
        
    def get_all_rules(self):
        LOG.info("get_all_rules")
        raise NotImplementedError()
    
    def exit(self):
        LOG.info("exit")
        raise NotImplementedError()