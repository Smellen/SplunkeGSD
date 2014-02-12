import unittest
import ConfigParser
import urllib2

class TestControllerDefault(unittest.TestCase):

	def testIndex(self):
		config = ConfigParser.ConfigParser()
		config.read("/home/www-data/web2py/applications/SplunkeGSD/application.config")
		fromFile = config.get("Main-Config","Test-String")
		try:
			webData = urllib2.urlopen('http://localhost:8000/SplunkeGSD')
		except urllib2.HTTPError as e:
			print e
			webData = e


		self.assertEqual(fromFile, webData.read())



if __name__ == '__main__':
	unittest.main()
