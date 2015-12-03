
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
    def __init__(self, count=-1, period=5, start=None, end=None):
        """

        :param count: -1 means forever
        :param period: N sec
        :param start: datetime, None mean now
        :param end: datetime, None mean forever
        """



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
