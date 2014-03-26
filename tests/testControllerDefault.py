import unittest
import ConfigParser
import urllib2
import imp
import sys
import os

default = imp.load_source('default', 'controllers/default.py')
team = imp.load_source('team', 'controllers/classes/team.py')
module = imp.load_source('module', 'controllers/classes/module.py')

os.chdir('../..')


class TestControllerDefault(unittest.TestCase):
		
	def testsave_game(self): 
		report = [['', 'Actual', 'Estimated'], ['Dublin: Test Module', '234.7', '200'], ['Total Effort', '234.7', '200']]
		budget = [['Cost', '7175.0', '8968.8']]
		revenue = [['Revenue', '500000.0', '500000.0']]
		files = [name for name in os.listdir('applications/SplunkeGSD/saved_game_reports')]
		blah = default.save_game_report_cal(report, budget, revenue)
		new_files = [name for name in os.listdir('applications/SplunkeGSD/saved_game_reports/')]
		self.assertTrue(len(new_files)-len(files) ==1)#check only one file is created
		fil = list( set(new_files)- set(files))		
		self.assertFalse(os.stat('applications/SplunkeGSD/saved_game_reports/'+str(fil[0])).st_size==0) 
		os.remove('applications/SplunkeGSD/saved_game_reports/'+str(fil[0]))
		
	def testload_game_cal(self): 
		self.assertTrue(True)

	def testview(self): 
		self.assertTrue(True)

	def testview_game(self):
		self.assertTrue(True)

	def testGetDailyDevPeriod(self):
		period = default.getDailyDevPeriod()
		self.assertIsNotNone(period)
		self.assertIsInstance(period, float) 

	def testGetFinalRevenue(self):
		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		bob.applyEffort()
		revenue = default.getFinalRevenue([bob], 1000000)
		self.assertIsInstance(revenue, str)
		self.assertNotEqual(revenue, '')

		tmp = float(revenue)
		self.assertIsInstance(tmp, float)

	def testGetExpectedBudget(self):
		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		bob.applyEffort()
		bud = default.getExpectedBudget([bob]*2)

		self.assertIsNotNone(bud)
		self.assertIsInstance(bud, float)

	def testGetTotalCost(self):

		config = ConfigParser.ConfigParser()
		config.read("applications/SplunkeGSD/application.config")
		cost_of_dev = config.get('Developer', 'Cost_Per_Day')

		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		
		lst = [bob]*2
		days = 5
		cost = default.getTotalCost(lst, 5)

		self.assertEqual(cost, (20*float(cost_of_dev)*days))



if __name__ == '__main__':
	unittest.main()
