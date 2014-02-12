import random

tasks = ["Design", "Implementation", "Unit Test", "Integration","System Test", "Deployment", "Acceptance Test"]

class module:

    def __init__(self, nm, estimate):
        self.name = nm
        self.test = "I love this"
        self.progress = 0
        self.estimateEffort = estimate
        self.actualEffort = (((random.random()/2) - 0.25) * estimate) + estimate

        #print self.actualEffort

	def progress(self, val):
		self.progress += val

	def changeActual(self, change):
		self.actualEffort  += change
        
    def getProgress(self): 
        prog = float(self.progress/self.actualEffort)
        if prog < 15: 
            return "Design"
        elif prog < 30: 
            return "Implementation" 
        elif prog < 40: 
            return "Unit Test"
        elif prog < 55: 
            return "Integration"
        elif prog < 70: 
            return "System Test"
        elif prog < 85: 
            return "Deployment" 
        elif prog < 100: 
            return "Acceptance Test"
        else: 
            return "Complete"

    def __repr__(self):
        ret =str(self.name) + ' is '+str(self.progress)+' of '+str(self.actualEffort)+' done. Stage: '+str(self.getProgress())
        return ret

if __name__ == "__main__":
	module(50)
