import unittest
import os
import imp

team = imp.load_source('team', 'controllers/classes/team.py')
module = imp.load_source('module', 'controllers/classes/module.py')
class TestTeam(unittest.TestCase):
	
	def testAddingModules(self):
		bob = team.team(10, 'dublin', 10) 
		mod = module.module('Test Module', 50) 
		lst = [mod]*10
		
		for m in lst: 
			bob.addModule(m)

		self.assertEqual(10, len(bob.currentModules))

	def testRemoveModules(self):
		mod1 = module.module("TestMod", 20)
		mod2 = module.module("AnotherTest", 40)
		bob = team.team(10, 'dublin', 10, [mod1, mod2])
		self.assertEqual(2, len(bob.currentModules))

		bob.removeModule(mod1)
		self.assertEqual(1, len(bob.currentModules))

	def testApplyEffort(self):
		bob = team.team(10, 'dublin', 10, [module.module('testModule', 40), module.module('anotherTestModule', 65)])
		effortList = []
		newEffortList = []
		for mod in bob.currentModules:
			effortList.append(mod.progress)

		bob.applyEffort()
		for mod in bob.currentModules:
			newEffortList.append(mod.progress)
			
		for i in xrange(len(bob.currentModules)):
			self.assertGreater(newEffortList[i], effortList[i]) 

	def testIsFinished(self):
		mod1 = module.module("TestMod", 20)
		mod2 = module.module("AnotherTest", 40)
		bob = team.team(10, 'dublin', 10, [mod1, mod2])

		self.assertFalse(bob.isFinished())

		for m in bob.currentModules:
			m.progress = m.actualEffort

		self.assertTrue(bob.isFinished())

	def testGetStatus(self):
		mod1 = module.module("TestMod", 20)
		mod2 = module.module("AnotherTest", 40)
		bob = team.team(10, 'dublin', 10, [mod1, mod2])

			
		validTasks= [0, 1, 2]
		for i in range(20):
			stat = bob.getStatus()
			for s in stat:
				self.assertIn(s, validTasks)
			bob.applyEffort()

	def testCalcDaysLeft(self):
		mod1 = module.module("TestMod", 20)
		mod2 = module.module("AnotherTest", 40)
		bob = team.team(10, 'dublin', 10, [mod1, mod2])

		for i in range(10):
			bob.calcDaysLeft()
			for m in bob.currentModules:
				self.assertTrue(isinstance(m.daysLeft, int))
			bob.applyEffort()
		

if __name__ == '__main__':
	unittest.main()
