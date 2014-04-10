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

def calculatepfail(listofteams, home="Dublin"):
    conf = open_conf()
    const = float(conf.get('Problems', 'probability'))
    prob = {}
    for team in listofteams:
        prob[team] = []
        if team.lower() != home.lower():
            value = json.loads(conf.get('Global - '+home, team))
            fail = value[0] + value[1]
            for val in value[2]:
                fail = fail + val
            temp = 1 + fail
            p_fail = fail / temp
            p_fail = p_fail * const
            prob[team].append(p_fail) #original p_fail
            prob[team].append(p_fail) #original p_fail
            prob[team].append(0) #i_j
        else:
            prob[team] = []
            prob[team].append(0.85)
            prob[team].append(0.85)
            prob[team].append(0)
    return prob

def generateIntervention(listoflocations):
    finaldict = {}
    intev = {}
    conf = open_conf()
    items = conf.items('Graphical Distance Interventions')
    for val in items: 
        print "".join(val[0].split(' '))
    for location in listoflocations:
        finaldict[location] = intev
    return finaldict

def addIntervention():
    intervention = request.args[0]
    location = request.args[1]
    value = session.interventions[location][intervention][1] #i_j value
    session.prob[location][2] = session.prob[location][2] + value
    calculateprob(session.prob)
    #add cost
    del session.interventions[location][intevention]
    return "Intervention Applied"

def calculateprob(teamprob): #probablility for home? {'location':[prob, org p_fail, i_j ]}
    for team in teamprob: #recalculates for each
        values = teamprob[team]
        temp = 1 + values[2]
        i = values[2] / temp
        temp1 = values[1]*i
        teamprob[team][0] = temp1
    return teamprob

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
    session.first = False
    session.cost = 0
    session.interventions = {}
    loct = [x.location for x in session.test]
    session.prob= calculatepfail(loct)
    new_team = team.team(10, 'dublin', getDailyDevPeriod())
    new_team.addModule(mod)
    new_team.calcDaysLeft()
    session.test.append(new_team)
    session.budget = getExpectedBudget(session.test)
    return
    
def save_game_report():
    save_game_report_cal(session.d_report, session.d_budget, session.d_revenue)
    redirect(URL('view'))

def save_game_report_cal(report, budget, revenue):
    try:
        f = open(strftime("applications/SplunkeGSD/saved_game_reports/%Y-%m-%d-%H:%M:%S", gmtime())+'.txt', 'w')
    except: 
        f = open(strftime("saved_game_reports/%Y-%m-%d-%H:%M:%S", gmtime())+'.txt', 'w') #for testing
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

def getFinalRevenue(listOfTeams, revenue=None, days=None, estimate_days=None):
    if revenue != None:
        rev = revenue
        day=days
        esti = estimate_days
    else:
        rev = session.revenue
        day = session.day
        esti = session.estimate_day
    #if int(day) > int(esti):
    num_days_late = int(day)-int(esti)
    temp = 6 - float((num_days_late/30))
    temp1 = float(rev/12)
    return [str("{:,.2f}".format(float(temp*temp1))), float(temp*temp1)]
    #else:
    #    return str(rev/2)

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
    try: 
        result = os.listdir("applications/SplunkeGSD/saved_game_reports")
    except: 
        result = os.listdir("saved_game_reports")
    result2=[]
    details = {}
    for i in result:
        i = i.strip() #remove space
        filename, extension = os.path.splitext(i)
        try:
            f = open('applications/SplunkeGSD/saved_game_reports/'+i, 'r')
        except: 
            f = open('saved_game_reports/'+i, 'r')
        contents = f.read()
        temp = contents.splitlines()
        details[filename]=[]
        for line in temp[2:]: #remove banners
            blah = line.split(',')
            details[filename].append(blah)
    return dict (title='Saved End of Game Reports', result2=details)


def problemSimulator(listOfTeams):
    config = open_conf()
    prob = config.get('Problems', 'probability')
    if len(listOfTeams) > 0:
        tmp = random.random()
        if tmp > float(prob):
            teamNum = int(random.random()*len(listOfTeams))
            modNum = int(random.random()*len(listOfTeams[teamNum].currentModules))
            listOfTeams[teamNum].currentModules[modNum].hadProblem = 1

    return False

def get_locations():
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
    generateIntervention(['Dublin', 'New York'])
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
        final = [0,0]
    else:
        if session.first == False:
            session.day += 1
            session.first = True
        final = getFinalRevenue(session.test)
    session.cost = getTotalCost(session.test, 1, session.cost)
    budgetReport = [["Cost", str("{:,.2f}".format(float(session.cost))) , str("{:,.2f}".format(float(session.budget)))]]
    revenueReport = [["Revenue", str(final[0]), str("{:,.2f}".format(float(session.revenue/2)))]]
    session.d_report = teamEstimatesAndProgresses
    session.d_budget = budgetReport
    session.d_revenue = revenueReport
    amount = str("{:,.2f}".format(((float(final[1]) + float(session.budget)) - float(session.cost))))
    final_rev =  str("{:,.2f}".format(float(final[1]) - (float(session.revenue/2))))
    final_cost = session.cost - session.budget
    problemSimulator(session.test)
    return dict(title='Global Software Tycoon', saved=session.saved, amount=amount, final_rev= final_rev, final_cost=final_cost, esti = session.estimate_day, modules=modules, final=final[0],  cost= str("{:,.0f}".format(float(session.cost))), the_revenue=session.revenue, the_budget= str("{:,.2f}".format(float(session.budget))), locations=location, completed=complete, report=teamEstimatesAndProgresses, budget=budgetReport, revenue=revenueReport, day=session.day)

def getTotalCost(listOfTeams, numDays, totalcost):
    config=open_conf()
    cost_of_dev = config.get('Developer', 'Cost_Per_Day')
    number_of_devs = 0
    for team in listOfTeams:
        number_of_devs = number_of_devs + team.teamSize
    return totalcost + (number_of_devs * float(cost_of_dev) * numDays)

def open_conf():
    config = ConfigParser.ConfigParser()
    try:
        config.read("applications/SplunkeGSD/application.config")
        test = config.get('Problems', 'probability') #forcing it to try it 
    except:
        config.read("application.config")
    return config

def view_game():
    responses = view_game_cal(session.estimate_day, session.test, session.day, session.cost)
    session.estimate_day = responses[3]
    return dict(title='Global Software Tycoon', esti = session.estimate_day, completed="false", budget=str("%.0f" % session.budget), cost=str("%.0f" % responses[0]),  the_revenue=session.revenue, modules=responses[2], locations=responses[1],day=session.day)

def view_game_cal(estimate_day, test, day, the_cost):
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
    cost = getTotalCost(test, 0, the_cost)
    return [cost, location, modules, estimate_day]

def config_game():
    try: 
        result = os.listdir("applications/SplunkeGSD/scenarios")
    except:
        result = os.listdir("scenarios/")
    result2=[]
    data = {}
    details = {}
    for i in result:
        i = i.strip() #remove space
        filename, extension = os.path.splitext(i)
        result2.append(filename)
    for the_file in result2: #for file in the list
        details[the_file]=[] #to put the information
        try: 
            string = "applications/SplunkeGSD/scenarios/"+the_file+".json"
            f=open(string)
        except: 
            string = "scenarios/"+the_file+".json"
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
    try: 
        string = "applications/SplunkeGSD/scenarios/"+file_id+".json"
        f=open(string)
    except: 
        string = "scenarios/"+file_id+".json"
        f=open(string)
    data = json.load(f)
    try: #web2py functionality
        session.test = []
        session.day = 0
        session.saved = "false"
        session.pre = "true"
        session.first = False
        session.cost = 0
        session.interventions = {}
        session.revenue = data['Game']['expected_revenue']
        projectType = data['Game']+['projectType']
        loct = [x.location for x in session.test]
        session.prob= calculatepfail(loct)
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

def emailQuery():
    tmp = request.args[0].replace("_", " ")
    lst = ['moscow', 'minsk', 'shanghai', 'tokyo', 'bangalore']
    if request.args[0] in lst:
        return "Yes, on schedule"
    for team in [x for x in session.test if x.location == tmp]:
        if team.getStatus() == [0]:
            return "Yes"
        else:
            return "No"
