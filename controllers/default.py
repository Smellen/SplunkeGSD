# -*- coding: utf-8 -*-
from __future__ import division
import ConfigParser
import applications.SplunkeGSD.controllers.classes.module as module
import applications.SplunkeGSD.controllers.classes.team as team
import subprocess
import os
import json
import ast
import unicodedata


def new_game(): # acts like initialisation. session.variablename allows the variable to be
 #accessed between refreshes.
    mod = module.module('Test Module', 200)
    te = mod.actualEffort
    session.test = []
    session.day = 0
    session.pre = "false"
    new_team = team.team(10, 'dublin', getDailyDevPeriod())
    new_team.addModule(mod)
    new_team.calcDaysLeft()
    print new_team.currentModules[0].daysLeft
    session.test.append(new_team)
    session.budget = getExpectedBudget()
    redirect(URL('view_game'))

def getDailyDevPeriod():
    config = ConfigParser.ConfigParser()
    config.read("applications/SplunkeGSD/application.config")
    return float(config.get('Development Period', 'Effort'))

def getExpectedBudget():
    avg_developer_effort_day = getDailyDevPeriod()
    number_of_devs = 0
    module_estimated_effort = 0
    for team in session.test:
        number_of_devs = number_of_devs + team.teamSize
        for mod in team.currentModules: 
            module_estimated_effort = module_estimated_effort + mod.estimateEffort
    print "module: "+ str(module_estimated_effort)
    print "devs: "+ str(number_of_devs)
    print "avg: "+ str(avg_developer_effort_day)
    temp = avg_developer_effort_day * number_of_devs
    print temp
    expected_budget = module_estimated_effort / temp
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
    teamEstimatesAndProgresses = [["", "Actual Effort", "Estimated Effort"]]
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
    budgetReport = [["Budget", "", ""]];
    revenueReport = [["Revenue", "", ""]];
    complete = "true" if isComplete else "false"
    if complete == "false":
        session.day += 1
    location = list(statuses.values())
    for team in session.test:
        for mod in team.currentModules:
            print mod.daysLeft
    return dict(title=T('Home'), modules=modules, locations=location, completed=complete, report=teamEstimatesAndProgresses, budget=budgetReport, revenue=revenueReport, day=session.day)


def view_game():
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
    teamEstimatesAndProgresses = []
    for team in session.test:
         statuses[team.location].append(team.getStatus())
         modules.append((team.location, team.currentModules, team.teamSize))
         isComplete = isComplete and team.isFinished()
         estimateAndProgress = []
         for mod in team.currentModules:
                estimateAndProgress.append([mod.name.encode("ascii"), mod.progress, mod.estimateEffort])
         teamEstimatesAndProgresses.append([team.location, estimateAndProgress])
    complete = "true" if isComplete else "false"
    location = list(statuses.values())
    return dict(title=T('Home'), budget=session.budget, modules=modules, pre=session.pre, locations=location,day=session.day, completed=complete, report=teamEstimatesAndProgresses)


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
        for te in data['Game']:
            dict1 = data['Game'][te]
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
    session.pre = "true"
    #read data in put in session.test
    for te in data['Game']:
        dict = data['Game'][te]
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

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
