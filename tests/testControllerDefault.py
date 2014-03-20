import unittest
import ConfigParser
import urllib2
import imp
import sys
import os

os.environ['TESTING'] = '1'

default = imp.load_source('default', 'controllers/default.py')
team = imp.load_source('team', 'controllers/classes/team.py')
module = imp.load_source('module', 'controllers/classes/module.py')

os.chdir('../..')


class TestControllerDefault(unittest.TestCase):

	def testGetDailyDevPeriod(self):
		period = default.getDailyDevPeriod()
		self.assertIsNotNone(period)
		self.assertIsInstance(period, float) 


if __name__ == '__main__':
	unittest.main()
