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
                      'get_all_rules']

    def add_rule(self):
        LOG.info("add_rule")
        raise NotImplemented()
    
    def del_rule(self):
        LOG.info("add_rule")
        raise NotImplemented()
        
    def update_rule(self):
        '''
        will stop PeriodicTask, update DB and apply_rule()
        '''
        LOG.info("update_rule")
        raise NotImplemented()
        
    def get_rule(self):
        LOG.info("get_rule")
        raise NotImplemented()
        
    def get_all_rules(self):
        LOG.info("get_all_rules")
        raise NotImplemented()
    
    