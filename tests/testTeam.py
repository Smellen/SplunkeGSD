import unittest
import os
import imp

team = imp.load_source('team', '/home/www-data/web2py/applications/SplunkeGSD/controllers/classes/team.py')
module = imp.load_source('module', '/home/www-data/web2py/applications/SplunkeGSD/controllers/classes/module.py')
class TestTeam(unittest.TestCase):
	
	def testAddingModules(self):
		bob = team.team(10, 10) 
		mod = module.module('Test Module', 50) 
		lst = [mod]*10
		
		for m in lst: 
			bob.addModule(m)

		self.assertEqual(10, len(bob.currentModules))

	def testRemoveModules(self):
		mod1 = module.module("TestMod", 20)
		mod2 = module.module("AnotherTest", 40)
		bob = team.team(10, 10, [mod1, mod2])
		self.assertEqual(2, len(bob.currentModules))

		bob.removeModule(mod1)
		self.assertEqual(1, len(bob.currentModules))

if __name__ == '__main__':
	unittest.main()
