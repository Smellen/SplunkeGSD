import unittest
import ConfigParser
import urllib2
import imp
import sys
import os

default = imp.load_source('default', 'controllers/default.py')
team = imp.load_source('team', 'controllers/classes/team.py')
module = imp.load_source('module', 'controllers/classes/module.py')

class TestControllerDefault(unittest.TestCase):
		
	def testsave_game_report_cal(self):
		report = [['', 'Actual', 'Estimated'], ['Dublin: Test Module', '234.7', '200'], ['Total Effort', '234.7', '200']]
		budget = [['Cost', '7175.0', '8968.8']]
		revenue = [['Revenue', '500000.0', '500000.0']] 
		files = [name for name in os.listdir('saved_game_reports/.')]
		blah = default.save_game_report_cal(report, budget, revenue)
		new_files = [name for name in os.listdir('saved_game_reports/')]
		self.assertTrue(len(new_files)-len(files) ==1)#check only one file is created
		fil = list( set(new_files)- set(files))
		self.assertFalse(os.stat('saved_game_reports/'+str(fil[0])).st_size==0) 
		os.remove('saved_game_reports/'+str(fil[0]))
	
	def testcalculatepfail(self): 
		lt = ['dublin', 'san francisco', 'bangalore']
		temp = default.calculatepfail(lt)
		self.assertTrue(len(temp) == len(lt))
		self.assertIsInstance(temp['dublin'][2], int)
		self.assertIsInstance(temp['dublin'][0], float)
		self.assertIsInstance(temp['dublin'][1], float)
	
	def testgenerateIntervention(self): 
		lt = ['dublin', 'san francisco', 'bangalore']
		temp = default.generateIntervention(lt) 
		self.assertTrue(len(lt) == len(temp))
		self.assertTrue(len(temp['dublin']) != 0)

	def testload_game_cal(self):
		blah = default.load_game_cal("game1")
		self.assertIsNotNone(blah)
		with self.assertRaises(IOError):
			blah = default.load_game_cal("EllenSmells")
	
	def testopen_conf(self): 
		conf = default.open_conf()
		self.assertIsNotNone(conf)

	def testget_locations(self): 
		locations = default.get_locations() 
		self.assertIsInstance(locations, dict)
		self.assertTrue(len(locations)>1)
	
	def testshow_saved_reports(self):
		test = default.show_saved_reports()
		self.assertIsInstance(test["title"], str) 
		self.assertIsInstance(test["result2"], dict)	

	def testconfig_game(self):
		temp = default.config_game()
		self.assertIsInstance(temp["title"], str)
		self.assertIsInstance(temp["data"], dict)
		self.assertIsInstance(temp["result"], list) 
		self.assertIsInstance(temp, dict)
	
	def testcalculateprob(self): 
		val = {'dublin': [0,3,4]}
		temp = default.calculateprob(val)
		self.assertTrue(temp['dublin'][0] != 0)
		self.assertTrue(temp['dublin'][1] == val['dublin'][1])
		self.assertTrue(temp['dublin'][2] == val['dublin'][2])

	def testview_game_cal(self): 
		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		bob.applyEffort()
		blah = default.view_game_cal(0, [bob], 0, 0)
		self.assertIsInstance(blah[3], str)

	def testproblemSimulator(self):
                bob = team.team(10, 'dublin', 10)
                mod1 = module.module('TestModule', 50)
                mod2 = module.module('TestModule2', 50)
                bob.addModule(mod1)
                bob.addModule(mod2)
                bob.applyEffort()
		result = default.problemSimulator([bob]) 
		self.assertIsInstance(result, bool)

	def testgetDailyDevPeriod(self):
		period = default.getDailyDevPeriod()
		self.assertIsNotNone(period)
		self.assertIsInstance(period, float) 

	def testgetFinalRevenue(self):
		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		bob.applyEffort()
		revenue = default.getFinalRevenue([bob], 1000000, 1, 2)
		self.assertIsInstance(revenue[0], str)
		self.assertIsInstance(revenue[1],float)
		self.assertNotEqual(revenue, '')

	def testgetExpectedBudget(self):
		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		bob.applyEffort()
		bud = default.getExpectedBudget([bob]*2)
		self.assertIsNotNone(bud)
		self.assertIsInstance(bud, float)

	def testgetTotalCost(self):
		config = ConfigParser.ConfigParser()
		config.read("application.config")
		cost_of_dev = config.get('Developer', 'Cost_Per_Day')
		bob = team.team(10, 'dublin', 10)
		mod1 = module.module('TestModule', 50)
		mod2 = module.module('TestModule2', 50)
		bob.addModule(mod1)
		bob.addModule(mod2)
		lst = [bob]*2
		days = 5
		cost = default.getTotalCost(lst, days, 0)
		self.assertEqual(cost, (20*float(cost_of_dev)*days))

if __name__ == '__main__':
	unittest.main()
