from __future__ import division
import random

tasks = ["Design", "Implementation", "Unit Test", "Integration","System Test", "Deployment", "Acceptance Test"]
stages = [0.15, 0.3, 0.4, 0.55, 0.7, 0.85, 1, 1] #Extra 1 for when the module is completed.
class module:

    def __init__(self, nm, estimate):
        self.name = nm
        self.test = "I love this"
        self.progress = 0
        self.daysLeft = None
        self.stage = "Unstarted"
        self.estimateEffort = estimate
        self.actualEffort = (((random.random()/2) - 0.25) * estimate) + estimate
        self.stageMarkers = self.calcStages(self.actualEffort)

        #print self.actualEffort
    def calcStages(self, effort):
        markers = []
        for stage in stages:
            markers.append(effort * stage)
        return markers

    def progress(self, val):
        self.progress += val

    def changeActual(self, change):
        self.actualEffort  += change

    def getProgress(self): 
        prog = float(self.progress/self.actualEffort)
        if prog < 0.15: 
            return "Design"
        elif prog < 0.30: 
            return "Implementation" 
        elif prog < 0.40: 
            return "Unit Test"
        elif prog < 0.55: 
            return "Integration"
        elif prog < 0.70: 
            return "System Test"
        elif prog < 0.85: 
            return "Deployment" 
        elif prog < 1: 
            return "Acceptance Test"
        else: 
            return "Complete"

    def effortLeftInStage(self, stage):
        return stageMarkers[stage] - self.progress

    def __repr__(self):
        stage = self.getProgress()
        ret =str(self.name) + ','+str("%.1f" % self.progress)+','+str("%.1f" % self.estimateEffort)+','+str(stage)+','+str(self.daysLeft)+','+str("%.1f" % self.actualEffort)
        return ret

    def isFinished(self):
        return self.progress >= self.actualEffort

if __name__ == "__main__":
	module(1, 50)
