import random

class module:
	
	def __init__(self, estimate):
		random.seed(None)
		self.test = "I love this"
		self.progress = 0
		self.EstimateEffort = estimate 
		self.ActualEffort = (((random.random()/2) - 0.25) * estimate) + estimate
		print self.ActualEffort

	def progress(self, val):
		self.progress += val
		
	def changeActual(self, change):
		self.ActualEffort  += change

if __name__ == "__main__":
	module(50)	




