# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from smart_house import sql_model
from periodic_task import PeriodicTask


class FinishCallback(object):
    """
    usually removes exhausted rule from table and
    removes 
    """
    def __init__(self, rule_id, rule_id_2_periodic_task_map):
        self.rule_id = rule_id
        self.rule_id_2_periodic_task_map = rule_id_2_periodic_task_map

    def __call__(self):
        pass


class IncrementTickCallback(object):
    """
    increments field Rule.cond_when_tick_count_done by Rule.id
    """
    def __init__(self, rule_id):
        self.rule_id = rule_id
        
    def __call__(self):
        pass
    
    
class DoCallback(object):
    """
    """
    def __init__(self,
                 cond_sql,
                 action_type,
                 handler_dev,
                 action,
                 priority,
                 sensors):
        self.cond_sql = cond_sql
        self.action_type = action_type
        self.handler_dev = handler_dev
        self.action = action
        self.priority = priority
        self.sensors = sensors
        
    def __call__(self):
        if sql_model.check_sql_condition(self.cond_sql):
            self.handler_dev.execute(self.action_type,
                                     self.action,
                                     self.priority)
    

def apply_db_rules(task_loop, handler_devs, sensors):
    '''
    apply_db_rules returns mapping rule_id TO PeriodicTask
    '''
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
    
    rule_id_2_periodic_task_map = {}
    db_session = sql_model.session()
    rules = db_session.query(sql_model.Rule)
    for rule in rules:
        apply_rule(task_loop, rule, rule_id_2_periodic_task_map,
                   handler_devs, sensors)


def apply_rule(task_loop, rule, rule_id_2_periodic_task_map,
               handler_devs, sensors):
    do_callback = DoCallback(rule.cond_sql,
                             rule.action_type,
                             handler_devs[rule.action_dev_id],
                             rule.action,
                             rule.priority,
                             sensors)#sensor maybe is redundant
    increment_tick_cb = IncrementTickCallback(rule.id)
    finish_cb = FinishCallback(rule.id, rule_id_2_periodic_task_map)
    do_callback_args = (
        rule.cond_sql,
        rule.action_type,
        handler_dev,
        action,
        priority,
        sensors
    )
    task = PeriodicTask(
        task_loop,
        rule.cond_when_start_time,
        do_callback, args=do_callback_args,
        finish_cb=finish_cb, finish_args=(rule.id, rule_id_2_periodic_task_map),
        count_increase_cb=increment_tick_cb, count_increase_cb_args=(rule.id, ),
        name=rule.name,
        count=rule.cond_when_tick_count,
        count_done=rule.cond_when_tick_count_done,
        period=rule.cond_when_tick_period,
        end_time=rule.cond_when_end_time
    )
    rule_id_2_periodic_task_map[rule.id] = task
    task.start()