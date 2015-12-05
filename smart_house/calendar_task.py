import datetime


class CalendarTask(object):
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
                 callback, args=(), kwargs={},
                 finish_cb=None, finish_args=(), finish_kwargs={},
                 name=None,
                 count=-1, period=5, start_time=None, end_time=None):
        """
        :param count: -1 means forever
        :param period: N sec
        :param start: datetime, None mean now
        :param end: datetime, None mean forever
        """
        self.name = name
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.count = count
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
        self.finish_cb = finish_cb
        self.finish_args = finish_args
        self.finish_kwargs = finish_kwargs
        self.running = False

    def start(self):
        self.running = True
        if self.start == None:
            self.start = datetime.datetime.now()

        # check if task expired:
        # 1. now() > start + count * period
        # 2. now() > end
        if count > 0:
            finish_datetime = self.start_time + \
                              datetime.timedelta(seconds=count*period)
            if datetime.datetime.now() > finish_datetime:
                return self.finish()
        if end and datetime.datetime.now() > end_time
            return self.finish()

        

    def finish(self):
        self.running = False
        if self.finish_cb:
            self.finish_cb(*self.finish_cb, **self.finish_args)

    def cancel(self):



    def join(self):

def wait_until(execute_it_now):
    while True:
        diff = (execute_it_now - datetime.now()).total_seconds()
        if diff <= 0:
            return
        elif diff <= 0.1:
            time.sleep(0.001)
        elif diff <= 0.5:
            time.sleep(0.01)
        elif diff <= 1.5:
            time.sleep(0.1)
        else:
            time.sleep(1)
