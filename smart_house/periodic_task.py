import logging
import threading


class PeriodicTask(object):
    """
    Python periodic Thread using Timer with instant cancellation
    """

    def __init__(self,
                 callback, args=(), kwargs={},
                 name=None,
                 period=1,
                 stop_on_error=False,
                 first_without_delay = True):
        self.name = name
        self.stop_on_error = stop_on_error
        self.first_iter_wo_delay = first_without_delay
        self.first_iter = False
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.period = period
        self.stop = False
        self.current_timer = None
        self.schedule_lock = threading.Lock()

    def start(self):
        """
        Mimics Thread standard start method
        """
        self.first_iter = True
        self.schedule_timer()

    def run(self):
        """
        Run desired callback and then reschedule Timer (if thread is not stopped)
        """
        error = False
        try:
            self.callback(*self.args, **self.kwargs)
        except Exception, e:
            error = True
            logging.exception("Exception in running periodic thread")
        if self.stop_on_error == True and error == True:
            logging.error("Periodic thread is stoped because of error")
            return
        with self.schedule_lock:
            if not self.stop:
                self.schedule_timer()

    def schedule_timer(self):
        """
        Schedules next Timer run
        """
        delay = self.period
        if self.first_iter_wo_delay == True and self.first_iter == True:
            delay = 0
        self.first_iter = False
        self.current_timer = threading.Timer(self.period, self.run)
        if self.name:
            self.current_timer.name = self.name
        self.current_timer.start()

    def cancel(self):
        """
        Mimics Timer standard cancel method
        """
        with self.schedule_lock:
            self.stop = True
            if self.current_timer is not None:
                self.current_timer.cancel()

    def join(self):
        """
        Mimics Thread standard join method
        """
        self.current_timer.join()
