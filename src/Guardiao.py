from Utils import getZabbixAPI, removeInvalidChar, getSessID
from json import dump
from time import sleep

ZabAPI = getZabbixAPI()
zabbixSessionID, phpSessionID = getSessID()

data = {}

def Applications():
    return ZabAPI.application.get(output="extend")

def Dashboards():
    return ZabAPI.dashboard.get(output="extend")

def dHost():
    return ZabAPI.dhost.get(output="extend")

def dService():
    return ZabAPI.dservice.get(output="extend")

def dRule():
    return ZabAPI.drule.get(output="extend")

def graph():
    return ZabAPI.graph.get(output="extend")

def graphprototype():
    return ZabAPI.graphprototype.get(output="extend")

def history():
    return ZabAPI.history.get(output="extend")

def host():
    return ZabAPI.host.get(output="extend")

def hostgroup():
    return ZabAPI.hostgroup.get(output="extend")

def hostinterface():
    return ZabAPI.hostinterface.get(output="extend")

def hostprototype():
    return ZabAPI.hostprototype.get(output="extend")

def iconmap():
    return ZabAPI.iconmap.get(output="extend")

def image():
    return ZabAPI.image.get(output="extend")

def item():
    return ZabAPI.item.get(output="extend")

def itemprototype():
    return ZabAPI.itemprototype.get(output="extend")

def discoveryrule():
    return ZabAPI.discoveryrule.get(output="extend")

def maintenance():
    return ZabAPI.maintenance.get(output="extend")

def map():
    return ZabAPI.map.get(output="extend")

def mediatype():
    return ZabAPI.mediatype.get(output="extend")

def problem():
    return ZabAPI.problem.get(output="extend")

def proxy():
    return ZabAPI.proxy.get(output="extend")

def screen():
    return ZabAPI.screen.get(output="extend")

def screenitem():
    return ZabAPI.screenitem.get(output="extend")

def hostinterface():
    return ZabAPI.hostinterface.get(output="extend")

def script():
    return ZabAPI.script.get(output="extend")

def service():
    return ZabAPI.service.get(output="extend")

def template():
    return ZabAPI.template.get(output="extend")

def templatescreen():
    return ZabAPI.templatescreen.get(output="extend")

def trend():
    return ZabAPI.trend.get(output="extend")

def trigger():
    return ZabAPI.trigger.get(output="extend")

def triggerprototype():
    return ZabAPI.triggerprototype.get(output="extend")

def user():
    return ZabAPI.user.get(output="extend")

def usergroup():
    return ZabAPI.usergroup.get(output="extend")

def usermacro():
    return ZabAPI.usermacro.get(output="extend")

def valuemap():
    return ZabAPI.valuemap.get(output="extend")

def webscenario():
    return ZabAPI.webscenario.get(output="extend")

def execAll():
    my_funcs = [Applications, Dashboards, dHost, dService, dRule, graph, graphprototype, 
    host,hostgroup, hostinterface, hostprototype, iconmap, image, #item, history, 
    itemprototype, maintenance, map, mediatype, problem,
    proxy, screen, screenitem, script, service, template,
    templatescreen, trigger, triggerprototype, #trend,
    user, usergroup, usermacro, valuemap#, webscenario
    ]
    for func in my_funcs:
        #print("Executing {}".format(str(func).split()[1]))
        funcData = func()
        if len(funcData) > 0:
            data[str(func).split()[1]] = funcData
        else:
            print("{} Returned no Data!".format(str(func).split()[1]))
    with open("data.json", "w") as json:
        dump(data, json, indent=4)



execAll()

