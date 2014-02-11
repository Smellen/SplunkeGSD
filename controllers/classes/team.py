# coding: utf8
# try something like
#def index(): return dict(message="hello from team.py")

class team:

    def __init__(self, size, location):
        self.teamSize = size
        self.currentModules = []
        #location should be loaded from the global config file
        self.localProductivity = location
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
        return self.teamSize * self.localProductivity * self.modifier

    def applyEffort(self):
        modEffort = float(self.totalEffort()) / len(self.currentModules)
        for module in self.currentModules:
            module.progress += modEffort
