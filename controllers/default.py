# -*- coding: utf-8 -*-
from __future__ import division
import ConfigParser
import os
import imp
try:
	import applications.SplunkeGSD.controllers.classes.module as module
	import applications.SplunkeGSD.controllers.classes.team as team
except:
    team = imp.load_source('team', 'controllers/classes/team.py')
    module = imp.load_source('module', 'controllers/classes/module.py')
import subprocess
import sys
import json
import ast
import unicodedata
from time import gmtime, strftime

import random

random.seed()

def new_game(): # acts like initialisation. session.variablename allows the variable to be accessed between refreshes.
    new_game_cal()
    redirect(URL('view_game'))

def new_game_cal():
    mod = module.module('Test Module', 200)
    te = mod.actualEffort
    session.test = []
    session.day = 0
    session.revenue = 1000000
    session.pre = "false"
    session.saved = "false"
    new_team = team.team(10, 'dublin', getDailyDevPeriod())
    new_team.addModule(mod)
    new_team.calcDaysLeft()
    session.test.append(new_team)
    session.budget = getExpectedBudget(session.test)
    problemSimulator()
    return
    
def save_game_report():
    save_game_report_cal(session.d_report, session.d_budget, session.d_revenue)
    redirect(URL('view'))

def save_game_report_cal(report, budget, revenue):
    f = open(strftime("applications/SplunkeGSD/saved_game_reports/%Y-%m-%d-%H:%M:%S", gmtime())+'.txt', 'w')
    f.write('\n')
    for i in report:
        f.write(str(i[0])+',')
        f.write(str(i[1])+',')
        f.write(str(i[2]))
        f.write('\n')
    for i in budget:
        f.write(str(i[0])+',')
        f.write(str(i[1])+',')
        f.write(str(i[2]))
    f.write('\n')
    for i in revenue:
        f.write(str(i[0])+',')
        f.write(str(i[1])+',')
        f.write(str(i[2]))
    f.write('\n')
    f.close()
    try:
        session.saved = "true"
    except:
        pass
    return

def getDailyDevPeriod():
    config=open_conf()
    return float(config.get('Development Period', 'Effort'))

def getFinalRevenue(listOfTeams, revenue = None):
    if revenue != None:
        rev = revenue
    else:
        rev = session.revenue
    number_of_days = 0
    for team in listOfTeams: 
        for mod in team.currentModules: 
            if mod.daysLeft < number_of_days: 
                number_of_days = mod.daysLeft
    days_late =  number_of_days * (-1)
    temp = 6 - (days_late/30)
    actual_revenue = temp * (rev /12)
    return str("%.2f" % actual_revenue)

def getExpectedBudget(listOfTeams):
    config=open_conf()
    cost_of_dev = config.get('Developer', 'Cost_Per_Day')
    avg_developer_effort_day = getDailyDevPeriod()
    module_estimated_effort = 0
    for team in listOfTeams:
        for mod in team.currentModules: 
            module_estimated_effort = module_estimated_effort + mod.estimateEffort
    temp = module_estimated_effort / avg_developer_effort_day 
    expected_budget = temp * float(cost_of_dev)
    expected_budget = expected_budget * 1.25
    return expected_budget 

def index():
    return dict(title='Home')

def show_saved_reports():
    result = os.popen("ls applications/SplunkeGSD/saved_game_reports").read()
    result1 = result.splitlines()
    result2=[]
    details = {}
    for i in result1:
        i = i.strip() #remove space
        filename, extension = os.path.splitext(i)
        f = open('applications/SplunkeGSD/saved_game_reports/'+i, 'r')
        contents = f.read()
        temp = contents.splitlines()
        details[filename]=[]
        for line in temp[2:]: #remove banners
            blah = line.split(',')
            details[filename].append(blah)
    return dict (title=T('Saved End of Game Reports'), result2=details)

def problemSimulator():
        config=open_conf()
	num = random.random()
	prob = config.get('Problems', 'probability')
	for team in session.test:
		for mod in team.currentModules:
			mod.hasProblem = random.random() >prob
			print mod.hasProblem

def generateEndOfGameReport():
    pass

"""def get_locations(): 
    config=open_conf()
    fromFile = config.items('Location')
    locations = {}
    for loc in fromFile:
         name, pos = loc
         locations[name.rstrip()] = ast.literal_eval(pos)
    return locations

def view():
    modules = []
    location = get_locations()
    isComplete = True
    teamEstimatesAndProgresses = [["", "Actual", "Estimated"]]
    totEstimate = 0
    totActual = 0
    for team in session.test:
        team.applyEffort()
        modules.append((team.location, team.currentModules, team.teamSize, team.getStatus(), location[team.location]))
        isComplete = isComplete and team.isFinished()
        for mod in team.currentModules:
             splitLoc = team.location.split(" ")
             capLoc = ""
             for word in splitLoc:
                 capped = word.capitalize()
                 capLoc += capped
             teamEstimatesAndProgresses.append([capLoc +": "+ mod.name.encode("ascii"), str("%.1f" % mod.progress), str(mod.estimateEffort)])
             totEstimate += mod.estimateEffort
             totActual += mod.progress
    teamEstimatesAndProgresses.append(["Total Effort", str("%.1f" % totActual), str(totEstimate)])
    complete = "true" if isComplete else "false"
    if complete == "false":
        session.day += 1
        final = 0
    else:
        final = getFinalRevenue(session.test)
    cost = getTotalCost(session.test, session.day)
    budgetReport = [["Cost", str("%.1f" % cost), str("%.1f" % session.budget)]];
    revenueReport = [["Revenue", str("%.1f" % float(final)), str("%.1f" % (session.revenue/2))]];
    session.d_report = teamEstimatesAndProgresses
    session.d_budget = budgetReport
    session.d_revenue = revenueReport
    amount = str("%.2f" % ((float(final) + float(session.budget)) - float(cost)))
    final_rev =  (float(session.revenue)/2) - float(final)
    final_cost = session.budget - cost
    print modules
    return dict(title='Team Splunke Game', saved=session.saved, amount=amount, final_rev=final_rev, final_cost=final_cost, esti = session.estimate_day, modules=modules, final=final,  cost=cost, the_revenue=session.revenue, the_budget=str("%.1f" % session.budget), locations=location, completed=complete, report=teamEstimatesAndProgresses, budget=budgetReport, revenue=revenueReport, day=session.day)"""

def view():
    modules = []
    statuses = {}
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    fromFile = config.items('Location')
    for loc in fromFile:
         name, pos = loc
         name.rstrip()
         statuses.update({name: ast.literal_eval(pos)})
    isComplete = True
    teamEstimatesAndProgresses = [["", "Actual", "Estimated"]]
    totEstimate = 0
    totActual = 0
    for team in session.test:
         team.applyEffort()
         statuses[team.location].append(team.getStatus())
         modules.append((team.location , team.currentModules, team.teamSize))
         isComplete = isComplete and team.isFinished()
         for mod in team.currentModules:
             splitLoc = team.location.split(" ")
             capLoc = ""
             for word in splitLoc:
                 capped = word.capitalize()
                 capLoc += capped
             teamEstimatesAndProgresses.append([capLoc +": "+ mod.name.encode("ascii"), str("%.1f" % mod.progress), str(mod.estimateEffort)])
             totEstimate += mod.estimateEffort
             totActual += mod.progress
    teamEstimatesAndProgresses.append(["Total Effort", str("%.1f" % totActual), str(totEstimate)])
    complete = "true" if isComplete else "false"
    if complete == "false":
        session.day += 1
        final = 0
    else:
        final = getFinalRevenue(session.test)
    cost = getTotalCost(session.test, session.day)
    budgetReport = [["Cost", str("%.1f" % cost), str("%.1f" % session.budget)]];
    revenueReport = [["Revenue", str("%.1f" % float(final)), str("%.1f" % (session.revenue/2))]];
    location = list(statuses.values())
    session.d_report = teamEstimatesAndProgresses
    session.d_budget = budgetReport
    session.d_revenue = revenueReport
    amount = str("%.2f" % ((float(final) + float(session.budget)) - float(cost)))
    final_rev =  (float(session.revenue)/2) - float(final)
    final_cost = session.budget -cost
    return dict(title='Team Splunke Game', saved=session.saved, amount=amount, final_rev=final_rev, final_cost=final_cost, esti = session.estimate_day, modules=modules, final=final,  cost=cost, the_revenue=session.revenue, the_budget=str("%.1f" % session.budget), locations=location, completed=complete, report=teamEstimatesAndProgresses, budget=budgetReport, revenue=revenueReport, day=session.day)

def getTotalCost(listOfTeams, numDays):
    config=open_conf()
    cost_of_dev = config.get('Developer', 'Cost_Per_Day')
    number_of_devs = 0
    for team in listOfTeams:
        number_of_devs = number_of_devs + team.teamSize
    return number_of_devs * float(cost_of_dev) * numDays 

def open_conf():
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    return config

def view_game():
    responses = view_game_cal(session.estimate_day, session.test, session.day)
    session.estimate_day = responses[3]
    return dict(title='Team Splunke Game', esti = session.estimate_day, completed="false", budget=str("%.1f" % session.budget), cost=responses[0],  the_revenue=session.revenue, modules=responses[2], locations=responses[1],day=session.day)

def view_game_cal(estimate_day, test, day):
    modules = []
    statuses = {}
    config=open_conf()
    fromFile = config.items('Location')
    estimate_day = 0
    for loc in fromFile:
         name, pos = loc
         name.rstrip()
         statuses.update({name: ast.literal_eval(pos)})
    for team in test:
         modules.append((team.location, team.currentModules, team.teamSize))
         for d_mod in team.currentModules:
             temp = str(d_mod).split(',')
             if int(temp[4]) >= int(estimate_day):
                    estimate_day = temp[4]
    location = list(statuses.values())
    cost = getTotalCost(test, day)
    return [cost, location, modules, estimate_day]

def config_game():
    result = os.popen("ls applications/SplunkeGSD/scenarios").read()
    result1 = result.splitlines()
    result2=[]
    details = {}
    for i in result1:
        i = i.strip() #remove space
        filename, extension = os.path.splitext(i)
        result2.append(filename)
    for the_file in result2: #for file in the list
        details[the_file]=[] #to put the information
        string = "applications/SplunkeGSD/scenarios/"+the_file+".json"
        f=open(string)
        data = json.load(f)
        projectType = data['Game']['projectType']
        for te in data['Game']['Teams']:
            dict1 = data['Game']['Teams'][te]
            listOfMods = []
            for mod in dict1['currentModules']:
                listOfMods.append((mod['name'], mod['estimate']))
            newTeam = (dict1['teamSize'], str(dict1['location']).lower(), listOfMods)
            details[the_file].append(newTeam)
    return dict(title='Pre-defined Games',result=result2, data=data["Game"], details=details)

def load_game():
    load_game_cal(None)
    redirect(URL('view_game'))

def load_game_cal(other_file_id):
    try:
        file_id = request.args[0]
    except:
        file_id = other_file_id
    string = "applications/SplunkeGSD/scenarios/"+file_id+".json"
    f=open(string)
    data = json.load(f)
    try: #web2py functionality
        session.test = []
        session.day = 0
        session.saved = "false"
        session.pre = "true"
        session.revenue = data['Game']['expected_revenue']
        projectType = data['Game']+['projectType']
    except:
        pass
    for te in data['Game']['Teams']:
        dict = data['Game']['Teams'][te]
        listOfMods = []
        for mod in dict['currentModules']:
            listOfMods.append(module.module(mod['name'], mod['estimate']))
        newTeam = team.team(dict['teamSize'], str(dict['location']).lower(), getDailyDevPeriod(), listOfMods)
        newTeam.calcDaysLeft()
        try:
            session.test.append(newTeam)
            session.budget = getExpectedBudget(session.test)
        except:
            pass
    return data
