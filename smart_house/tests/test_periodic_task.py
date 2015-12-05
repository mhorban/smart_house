import unittest

class TestPeriodicTask(unittest.TestCase):

    def setUp(self):
        super(TestPeriodicTask, self).setUp()

    def testTodo(self):
        self.assertEqual('foo', 'foo')
