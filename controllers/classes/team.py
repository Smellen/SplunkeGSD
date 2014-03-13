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
        self.stage = 0

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

    class ProjectTypeError(Exception):
        pass
    # ProjectType 0 = agile, 1 = waterfall, 2 = follow the sun
    def applyEffort(self, projectType):
        if(projectType) == 0:
            modEffort = float(self.totalEffort()) / len(self.currentModules)
            for module in self.currentModules:
                if module.progress < module.actualEffort:
                    module.progress += modEffort
                if module.progress >= module.actualEffort:
                    module.progress = module.actualEffort
                module.daysLeft = int((module.estimateEffort-module.progress) / modEffort)
        elif(projectType == 1):
            modEffort = float(self.totalEffort()) / len(self.currentModules)
            allFinished = True
            for module in self.currentModules:
                if module.progress < module.stageMarkers[self.stage]:
                    module.progress += modEffort
                    allFinished = False
                if module.progress >= module.actualEffort:
                    module.progress = module.actualEffort
            if allFinished:
                self.stage += 1
        elif(projectType == 2):
            pass
        else:
            raise ProjectTypeError

# 0 = Green, 1 = Yellow, 2 = Red.
    def getStatus(self):
        res = [0]
        for module in self.currentModules:
            if module.progress > module.estimateEffort and module.progress < module.actualEffort:
                res[0] = 1 #If any module late show yellow.
        return res

    def isFinished(self):
        res = True
        for module in self.currentModules:
            res = res and module.isFinished()
        return res
