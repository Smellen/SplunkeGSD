# -*- coding: utf-8 -*-

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
    mod = module.module('Test Module', 50)
    te = mod.actualEffort
    session.test = []
    new_team = team.team(10, 'dublin')
    new_team.addModule(mod)
    session.test.append(new_team)
    redirect(URL('view'))

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
    for team in session.test:
         team.applyEffort()
         statuses[team.location].append(team.getStatus())
         print team.getStatus()
         modules.append(team.currentModules)
    location = list(statuses.values())
    return dict(title=T('Home'), modules=modules, locations=location)

def config_game():
    result = os.popen("ls applications/SplunkeGSD/scenarios").read()
    result1 = result.splitlines()
    result2=[]
    for i in result1:
        i = i.strip() #remove space
        i = i.strip(".json") #remove the .json at end
        result2.append(i)
    return dict(title=T('Pre-defined Games'),result=result2)

def load_game():
    file_id = request.args[0]
    string = "applications/SplunkeGSD/scenarios/"+file_id+".json"
    f=open(string)
    data = json.load(f)
    session.test = []
    #read data in put in session.test
    for te in data['Game']:
        dict = data['Game'][te]
        listOfMods = []
        for mod in dict['currentModules']:
            listOfMods.append(module.module(mod['name'], mod['estimate']))
        newTeam = team.team(dict['teamSize'], str(dict['location']).lower(), listOfMods)
        session.test.append(newTeam)
    redirect(URL('view'))

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
