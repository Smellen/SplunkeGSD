# -*- coding: utf-8 -*-
from __future__ import division
import ConfigParser
import os
try:
	import applications.SplunkeGSD.controllers.classes.module as module
	import applications.SplunkeGSD.controllers.classes.team as team
except:
	pass

import subprocess
import json
import ast
import unicodedata
from time import gmtime, strftime 

def new_game(): # acts like initialisation. session.variablename allows the variable to be
 #accessed between refreshes.
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
    print new_team.currentModules[0].daysLeft
    session.test.append(new_team)
    session.budget = getExpectedBudget()
    redirect(URL('view_game'))

def save_game():
    f = open(strftime("applications/SplunkeGSD/saved_game_reports/%Y-%m-%d-%H:%M:%S", gmtime())+'.txt', 'w')
    f.write('\n')
    for i in session.d_report:
        f.write(str(i[0])+',')
        f.write(str(i[1])+',')
        f.write(str(i[2]))
        f.write('\n')
    for i in session.d_budget:
        print i
        f.write(str(i[0])+',')
        f.write(str(i[1])+',')
        f.write(str(i[2]))
    f.write('\n')
    for i in session.d_revenue: 
        f.write(str(i[0])+',')
        f.write(str(i[1])+',')
        f.write(str(i[2]))
    f.write('\n')
    f.close()
    session.saved = "true"
    redirect(URL('view'))
    
def getDailyDevPeriod():
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    return float(config.get('Development Period', 'Effort'))

def getFinalRevenue(listOfTeams, revenue = None):
    if revenue != None:
        session.revenue = revenue
    number_of_days = 0
    for team in listOfTeams: 
        for mod in team.currentModules: 
            if mod.daysLeft < number_of_days: 
                number_of_days = mod.daysLeft
    days_late =  number_of_days * (-1)
    temp = 6 - (days_late/30)
    actual_revenue = temp * (session.revenue /12)
    return str("%.2f" % actual_revenue)

def getExpectedBudget():
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    cost_of_dev = config.get('Developer', 'Cost_Per_Day')
    avg_developer_effort_day = getDailyDevPeriod()
    module_estimated_effort = 0
    for team in session.test:
        for mod in team.currentModules: 
            module_estimated_effort = module_estimated_effort + mod.estimateEffort
    print "module: "+ str(module_estimated_effort)
    print "avg: "+ str(avg_developer_effort_day)
    temp = module_estimated_effort / avg_developer_effort_day 
    print temp
    expected_budget = temp * float(cost_of_dev)
    print expected_budget
    expected_budget = expected_budget * 1.25
    return expected_budget 

def index():
    if 'default' in request.env.path_info: #ensures that the link is right
        new = 'new_game'
        config = 'config_game'
    else:
        new = 'default/new_game'
        config = 'default/config_game'

    return dict(title=T('Home'), new=new, config=config)

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
        for line in temp[3:]: #remove banners
            blah = line.split(',')
            details[filename].append(blah)
    return dict (title=T('Saved End of Game Reports'), result2=details)

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
    cost = getTotalCost()
    budgetReport = [["Cost", str("%.1f" % cost), str("%.1f" % session.budget)]];
    revenueReport = [["Revenue", str("%.1f" % float(final)), str("%.1f" % (session.revenue/2))]];
    location = list(statuses.values())
    for team in session.test:
        for mod in team.currentModules:
            print mod.daysLeft
    session.d_report = teamEstimatesAndProgresses
    session.d_budget = budgetReport
    session.d_revenue = revenueReport
    score = (float(final) + float(session.budget)) - float(cost)
    return dict(title=T('Team Splunke Game'), saved=session.saved, score=score, esti = session.estimate_day, modules=modules, final=final,  cost=cost, the_revenue=session.revenue, the_budget=str("%.1f" % session.budget), locations=location, completed=complete, report=teamEstimatesAndProgresses, budget=budgetReport, revenue=revenueReport, day=session.day)

def getTotalCost():
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    cost_of_dev = config.get('Developer', 'Cost_Per_Day')
    number_of_devs = 0
    for team in session.test:
        number_of_devs = number_of_devs + team.teamSize
    return number_of_devs * float(cost_of_dev) * session.day

def view_game():
    modules = []
    statuses = {}
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    fromFile = config.items('Location')
    session.estimate_day = 0
    for loc in fromFile:
         name, pos = loc
         name.rstrip()
         statuses.update({name: ast.literal_eval(pos)})
    isComplete = True
    teamEstimatesAndProgresses = []
    for team in session.test:
         statuses[team.location].append(team.getStatus())
         modules.append((team.location, team.currentModules, team.teamSize))
         for d_mod in team.currentModules:
             temp = str(d_mod).split(',')
             if int(temp[4]) >= int(session.estimate_day):
                    session.estimate_day = temp[4]
         isComplete = isComplete and team.isFinished()
         estimateAndProgress = []
         for mod in team.currentModules:
                estimateAndProgress.append([mod.name.encode("ascii"), mod.progress, mod.estimateEffort])
         teamEstimatesAndProgresses.append([team.location, estimateAndProgress])
    complete = "true" if isComplete else "false"
    location = list(statuses.values())
    cost = getTotalCost()
    return dict(title=T('Team Splunke Game'), esti = session.estimate_day, budget=str("%.1f" % session.budget), cost=cost,  the_revenue=session.revenue, modules=modules, pre=session.pre, locations=location,day=session.day, completed=complete, report=teamEstimatesAndProgresses)


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
    return dict(title=T('Pre-defined Games'),result=result2, data=data["Game"], details=details)

def load_game():
    file_id = request.args[0]
    string = "applications/SplunkeGSD/scenarios/"+file_id+".json"
    f=open(string)
    data = json.load(f)
    session.test = []
    session.day = 0
    session.saved = "false"
    session.pre = "true"
    projectType = data['Game']['projectType']
    session.revenue = data['Game']['expected_revenue']
    for te in data['Game']['Teams']:
        dict = data['Game']['Teams'][te]
        listOfMods = []
        for mod in dict['currentModules']:
            listOfMods.append(module.module(mod['name'], mod['estimate']))
        newTeam = team.team(dict['teamSize'], str(dict['location']).lower(), getDailyDevPeriod(), listOfMods)
        newTeam.calcDaysLeft()
        session.test.append(newTeam)
        session.budget = getExpectedBudget()
    redirect(URL('view_game'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
