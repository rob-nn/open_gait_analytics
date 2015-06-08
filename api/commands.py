from flask.ext.script import Command
import unittest
from oga_api.test_rest import TestRest

class TestCommand(Command):
    def run(self):
	print 'testing'
	"""suite = [unittest.TestLoader().loadTestsFromTestCase(TestRest)]
        unittest.TextTestRunner(verbosity=2).run(suite)a"""
