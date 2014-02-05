import unittest
import ConfigParser
import urllib2

class TestControllerDefault(unittest.TestCase):

	def testIndex(self):
		config = ConfigParser.ConfigParser()
		config.read("/home/www-data/web2py/applications/SplunkeGSD/application.config")
		fromFile = config.get("Main-Config","Test-String")

		webData = urllib2.urlopen('http://localhost/SplunkeGSD')



		self.assertEqual(fromFile, webData.read())



if __name__ == '__main__':
	unittest.main()
