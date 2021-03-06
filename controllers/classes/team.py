# coding: utf8
# try something like
#def index(): return dict(message="hello from team.py")
import ConfigParser


class team:

    def __init__(self, size, location, effectiveWorkingDay, modules=None):
        self.teamSize = size
        self.currentModules = []
        self.effectiveWorkingDay = effectiveWorkingDay
        if modules != None:
            for m in modules:
                self.currentModules.append(m)

        #location should be loaded from the global config file
        self.location = location
        self.localProductivity = 1
        self.modifier = 1

    def changeTeamSize(self, newSize):
        self.teamSize = newSize

    def changeModifier(self, newMod):
        self.modifier = newMod

    def removeModule(self, module):
        self.currentModules.remove(module)

    def addModule(self, module):
        self.currentModules.append(module)

    def totalEffort(self):
        return self.teamSize * self.localProductivity * self.modifier * self.effectiveWorkingDay

    def calcDaysLeft(self):
        modEffort = float(self.totalEffort()) / len(self.currentModules)
        for module in self.currentModules:
            module.daysLeft = int((module.estimateEffort - module.progress) / modEffort)

    def applyEffort(self):
        modEffort = float(self.totalEffort()) / len(self.currentModules)
        for module in self.currentModules:
            if module.progress < module.actualEffort and module.hasProblem:
                stage = module.getProgress()
                config = ConfigParser.ConfigParser()
                config.read("applications/SplunkeGSD/application.config")
                delay = float(config.get('Problems ' + stage, 'delay'))
                delay = (delay/100.0) + 1
                module.actualEffort = module.actualEffort * delay
                module.hasProblem = False
            if module.progress < module.actualEffort:
                module.progress += modEffort
            if module.progress >= module.actualEffort:
                module.progress = module.actualEffort
            module.daysLeft = int((module.estimateEffort-module.progress) / modEffort)

# 0 = Green, 1 = Yellow, 2 = Red.
    def getStatus(self):
        res = [0]
        for module in self.currentModules:
            if module.progress > module.estimateEffort and module.progress < module.actualEffort:
                res[0] = 1 #If any module late show yellow.
            if module.hasProblem == True:
                return [2]
        return res

    def isFinished(self):
        res = True
        for module in self.currentModules:
            res = res and module.isFinished()
        return res
