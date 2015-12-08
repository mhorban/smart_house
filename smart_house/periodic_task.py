import datetime
import logging
import threading
import time
import math

from oslo_config import cfg
from oslo_log import log as logging

from smart_house import sql_model

CONF = cfg.CONF

opts = [
    cfg.FloatOpt('periodic_task_loop_delay',
                  default=1.0,
                  help='Delay among applying all rules.'),
    ]

CONF.register_opts(opts)


class PeriodicTask(object):
    """
    each N period - mean start now and continue forever
    each N period start XX.XX.XXXX - mean start XX.XX.XXXX do forever
    X times each N period start XX.XX.XXXX - mean X times start XX.XX.XXXX with period N
    X times each N period start XX.XX.XXXX end YY.YY.YYYY - mean X times start XX.XX.XXXX  end YY.YY.YYYY with period N
    once - mean now once
    once start XX.XX.XX

    if period is more than 30 sec we use CalendarTask
    """

    def __init__(self,
                 periodic_task_loop,
                 start_time,
                 callback, args=(), kwargs={},
                 finish_cb=None, finish_args=(), finish_kwargs={},
                 count_increase_cb=None, count_increase_cb_args=(), count_increase_cb_kwargs={},
                 name=None,
                 count=-1, count_done=0, period=5, end_time=None):
        """
        :param count: -1 means forever
        :param period: N sec
        :param start: datetime, None mean now
        :param end: datetime, None mean forever
        """
        self.periodic_task_loop = periodic_task_loop
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.count = count
        self.count_done = count_done
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
        self.finish_cb = finish_cb
        self.finish_args = finish_args
        self.finish_kwargs = finish_kwargs
        self.running = False
        self.count_increase_cb = count_increase_cb
        self.count_increase_cb_args = count_increase_cb_args
        self.count_increase_cb_kwargs = count_increase_cb_kwargs
        self.time_of_last_call = self.start_time

    def start(self):
        self.running = True
        self._restart()
        
    def _restart(self):
        time_to_run = self._calc_next_call()
        if time_to_run:
            self._shedule_callback(time_to_run);
        else:
            self._finish()

    def _run(self):
        try:
            self.callback(*self.args, **self.kwargs)
        except Exception, e:
            logging.exception("Exception in running periodic thread")
        self.count_increase_cb(*count_increase_cb_args, **count_increase_cb_kwargs)
        self.count_done += 1
        self.time_of_last_call = datetime.datetime.now()
        if self.running:
            self._restart()

    def _shedule_callback(self, time_to_run):
        self.periodic_task_loop.shedule_task(time_to_run, self._run)
        
    def _cancel_sheduled_callback(self):
        self.periodic_task_loop.cancel_task(self._run)
    
    def _calc_next_call(self):
        # check if task expired:
        # 1. self.count_done > self.count
        # 2. now() > end_time
        # 3. now() > start_time + count * period
        if self.count_done > self.count:
            return None
        now = datetime.datetime.now()
        if self.count > 0:
            finish_datetime = self.start_time + \
                              datetime.timedelta(seconds=count*period)
            if now > finish_datetime:
                return None
        if self.end_time and now > end_time:
            return None
        
        # if start_time in the future return it
        if now < self.start_time:
            return self.start_time
        
        # calculate time of next call
        delta = now - self.time_of_last_call
        seconds_delta = math.ceil(delta.total_seconds() / self.period) * \
                        self.period
        return self.start_time + datetime.timedelta(seconds=seconds_delta)

    def cancel(self):
        self.running = False
        self._cancel_sheduled_callback()

    def is_running(self):
        return self.running

    def _finish(self):
        self.running = False
        if self.finish_cb:
            # finish_cb must delete rule from DB
            self.finish_cb(*self.finish_cb, **self.finish_args)
            
            
class PeriodicTaskLoop(object):
    def __init__(self):
        self._action_ordered_list = []
        self._thread = threading.Thread(self._loop)

    def start(self):
        self.running = True
        self._thread.start()
        
    def stop(self):
        self.running = False
    
    def shedule_task(self, time_to_run, task):
        self._action_ordered_list.append((time_to_run, task))
        # TODO add some ordered type and not make full reorder each time
        self._action_ordered_list.sort(
            cmp=lambda x, y: x[0].total_seconds() - y[0].total_seconds())
    
    def cancel_task(self, cb):
        for task in list(self._action_ordered_list):
            if task[1] == cb:
                self._action_ordered_list.remove(task)
    
    def _loop(self):
        while self.running:
            now = datetime.datetime.now()
            for task in list(self._action_ordered_list):
                if task[0] > now:
                    break
                callback = self._action_ordered_list.pop(0)[1]
                callback()
            time.sleep(CONF.periodic_task_loop_delay)
            
        