import random

tasks = ["Design", "Implementation", "Unit Test", "Integration","System Test", "Deployment", "Acceptance Test"]

class module:

    def __init__(self, nm, estimate):
        self.name = nm
        self.test = "I love this"
        self.progress = 0
        self.stage = "Unstarted"
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
            self.stage = "Design"
        elif prog < 30: 
            self.stage ="Implementation" 
        elif prog < 40: 
            self.stage ="Unit Test"
        elif prog < 55: 
            self.stage ="Integration"
        elif prog < 70: 
            self.stage ="System Test"
        elif prog < 85: 
            self.stage ="Deployment" 
        elif prog < 100: 
            self.stage ="Acceptance Test"
        else: 
            self.stage ="Complete"

    def __repr__(self):
        stage = self.getProgress()
        ret =str(self.name) + ' is '+str(self.progress)+' of '+str(self.actualEffort)+' done. Stage: '+str(stage)
        return ret

if __name__ == "__main__":
	module(50)
