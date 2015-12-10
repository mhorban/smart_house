import unittest
import datetime
import mock
import time

from smart_house import periodic_task


class TestPeriodicTask(unittest.TestCase):
    def setUp(self):
        super(TestPeriodicTask, self).setUp()

    def test_callbacks(self):
        callback = mock.MagicMock()
        args = ('arg_1', 'arg_2')
        kwargs = {'kwarg_1': 'kwarg_1', 'kwarg_2': 'kwarg_2'}
        finish_cb = mock.MagicMock()
        finish_args = ('finish_arg_1', 'finish_arg_2')
        finish_kwargs = {'finish_kwarg_1': 'finish_kwarg_1',
                         'finish_kwarg_2': 'finish_kwarg_2'}
        count_increase_cb = mock.MagicMock()
        count_increase_cb_args = ('increase_cb_arg_1', 'increase_cb_arg_2')
        count_increase_cb_kwargs = {'increase_cb_kwarg_1': 'increase_cb_kwarg_1',
                                    'increase_cb_kwarg_2': 'increase_cb_kwarg_2'}

        ptl = periodic_task.PeriodicTaskLoop()
        pt = periodic_task.PeriodicTask(ptl,
                 datetime.datetime.now() + datetime.timedelta(seconds=2),
                 callback, args=args, kwargs=kwargs,
                 finish_cb=finish_cb, finish_args=finish_args, finish_kwargs=finish_kwargs,
                 count_increase_cb=count_increase_cb,
                     count_increase_cb_args=count_increase_cb_args, 
                     count_increase_cb_kwargs=count_increase_cb_kwargs,
                 name='test',
                 count=4, count_done=1, period=2,
                 end_time=None)
        pt.start()
        ptl.start()
        time.sleep(8)
        ptl.stop()
        self.assertEquals(callback.mock_calls, 
                          [mock.call(*args, **kwargs),
                           mock.call(*args, **kwargs),
                           mock.call(*args, **kwargs)])
        finish_cb.assert_called_once_with(*finish_args, **finish_kwargs)
        self.assertEquals(count_increase_cb.mock_calls,
                          [mock.call(*count_increase_cb_args,
                                     **count_increase_cb_kwargs),
                           mock.call(*count_increase_cb_args,
                                     **count_increase_cb_kwargs),
                           mock.call(*count_increase_cb_args,
                                     **count_increase_cb_kwargs)])
                          
        
    def test_callbacks_2(self):
        callback = mock.MagicMock()
        args = ('arg_1', 'arg_2')
        kwargs = {'kwarg_1': 'kwarg_1', 'kwarg_2': 'kwarg_2'}
        finish_cb = mock.MagicMock()
        finish_args = ('finish_arg_1', 'finish_arg_2')
        finish_kwargs = {'finish_kwarg_1': 'finish_kwarg_1',
                         'finish_kwarg_2': 'finish_kwarg_2'}
        count_increase_cb = mock.MagicMock()
        count_increase_cb_args = ('increase_cb_arg_1', 'increase_cb_arg_2')
        count_increase_cb_kwargs = {'increase_cb_kwarg_1': 'increase_cb_kwarg_1',
                                    'increase_cb_kwarg_2': 'increase_cb_kwarg_2'}

        ptl = periodic_task.PeriodicTaskLoop()
        ptl.start()
        pt = periodic_task.PeriodicTask(ptl,
                 datetime.datetime.now() + datetime.timedelta(seconds=2),
                 callback, args=args, kwargs=kwargs,
                 finish_cb=finish_cb, finish_args=finish_args, finish_kwargs=finish_kwargs,
                 count_increase_cb=count_increase_cb,
                     count_increase_cb_args=count_increase_cb_args, 
                     count_increase_cb_kwargs=count_increase_cb_kwargs,
                 name='test',
                 count=4, count_done=1, period=2,
                 end_time=None)
        pt.start()
        time.sleep(8)
        ptl.stop()
        self.assertEquals(callback.mock_calls, 
                          [mock.call(*args, **kwargs),
                           mock.call(*args, **kwargs),
                           mock.call(*args, **kwargs)])
        finish_cb.assert_called_once_with(*finish_args, **finish_kwargs)
        self.assertEquals(count_increase_cb.mock_calls,
                          [mock.call(*count_increase_cb_args,
                                     **count_increase_cb_kwargs),
                           mock.call(*count_increase_cb_args,
                                     **count_increase_cb_kwargs),
                           mock.call(*count_increase_cb_args,
                                     **count_increase_cb_kwargs)])

    def test_cancel(self):
        callback = mock.MagicMock()
        args = ('arg_1', 'arg_2')
        kwargs = {'kwarg_1': 'kwarg_1', 'kwarg_2': 'kwarg_2'}
        finish_cb = mock.MagicMock()
        finish_args = ('finish_arg_1', 'finish_arg_2')
        finish_kwargs = {'finish_kwarg_1': 'finish_kwarg_1',
                         'finish_kwarg_2': 'finish_kwarg_2'}
        count_increase_cb = mock.MagicMock()
        count_increase_cb_args = ('increase_cb_arg_1', 'increase_cb_arg_2')
        count_increase_cb_kwargs = {'increase_cb_kwarg_1': 'increase_cb_kwarg_1',
                                    'increase_cb_kwarg_2': 'increase_cb_kwarg_2'}

        ptl = periodic_task.PeriodicTaskLoop()
        ptl.start()
        pt = periodic_task.PeriodicTask(ptl,
                 datetime.datetime.now() + datetime.timedelta(seconds=2),
                 callback, args=args, kwargs=kwargs,
                 finish_cb=finish_cb, finish_args=finish_args, finish_kwargs=finish_kwargs,
                 count_increase_cb=count_increase_cb,
                     count_increase_cb_args=count_increase_cb_args, 
                     count_increase_cb_kwargs=count_increase_cb_kwargs,
                 name='test',
                 count=4, count_done=1, period=2,
                 end_time=None)
        pt.start()
        pt.stop()
        time.sleep(8)
        ptl.stop()
        self.assertFalse(callback.called)
        self.assertFalse(count_increase_cb.called)
        finish_cb.assert_called_once_with(*finish_args, **finish_kwargs)


class TestPeriodicTaskLoop(unittest.TestCase):
    def setUp(self):
        super(TestPeriodicTaskLoop, self).setUp()

    def test_init(self):
        ptl = periodic_task.PeriodicTaskLoop()

    def test_start(self):
        ptl = periodic_task.PeriodicTaskLoop()
        ptl.start()
        self.assertTrue(ptl.running)
        self.assertTrue(ptl._thread.is_alive())
        ptl.stop()

    def test_stop(self):
        ptl = periodic_task.PeriodicTaskLoop()
        ptl.start()
        ptl.stop()
        self.assertFalse(ptl.running)
        time.sleep(3)
        self.assertFalse(ptl._thread.is_alive())

    def test_shedule_cancel_task_before_start(self):
        def cb1():
            pass
        def cb2():
            pass
        ptl = periodic_task.PeriodicTaskLoop()
        dtime = [datetime.datetime(year=2015, month=12, day=1),
                 datetime.datetime(year=2015, month=12, day=2)]
        ptl.shedule_task(dtime[1], cb1)
        ptl.shedule_task(dtime[0], cb2)
        self.assertEqual(ptl._action_ordered_list[0][0], dtime[0])
        self.assertEqual(ptl._action_ordered_list[1][0], dtime[1])
        self.assertEqual(len(ptl._action_ordered_list), 2)

        ptl.cancel_task(cb1)
        ptl.cancel_task(cb2)
        self.assertEqual(len(ptl._action_ordered_list), 0)

    def test_loop(self):
        call_list = []
        def cb2():
            call_list.append('cb2')
        def cb4():
            call_list.append('cb4')
        def cb3():
            call_list.append('cb3')
        def cb3_after_start():
            call_list.append('cb3_after_start')
        def cb4_after_start():
            call_list.append('cb4_after_start')

        now = datetime.datetime.now()
        dtime2 = now + datetime.timedelta(seconds=2)
        dtime4 = now + datetime.timedelta(seconds=4)
        dtime3 = now + datetime.timedelta(seconds=3)

        ptl = periodic_task.PeriodicTaskLoop()
        ptl.shedule_task(dtime2, cb2)
        ptl.shedule_task(dtime4, cb4)
        ptl.shedule_task(dtime3, cb3)
        ptl.start()
        ptl.shedule_task(dtime3, cb3_after_start)
        ptl.shedule_task(dtime4, cb4_after_start)
        time.sleep(1)
        ptl.cancel_task(cb4_after_start)
        time.sleep(5)
        ptl.stop()
        self.assertTrue(call_list == ['cb2', 'cb3', 'cb3_after_start', 'cb4'] or
                        call_list == ['cb2', 'cb3_after_start', 'cb3', 'cb4'],
                        msg='actual call_list == %s'%str(call_list))