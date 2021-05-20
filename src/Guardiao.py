from Utils import ZabbixAPI
from json import dump


data = {}

def Applications():
    return ZabbixAPI.application.get(output="extend")

def Dashboards():
    return ZabbixAPI.dashboard.get(output="extend")

def dHost():
    return ZabbixAPI.dhost.get(output="extend")

def dService():
    return ZabbixAPI.dservice.get(output="extend")

def dRule():
    return ZabbixAPI.drule.get(output="extend")

def graph():
    return ZabbixAPI.graph.get(output="extend")

def graphprototype():
    return ZabbixAPI.graphprototype.get(output="extend")

def history():
    return ZabbixAPI.history.get(output="extend")

def host():
    return ZabbixAPI.host.get(output="extend")

def hostgroup():
    return ZabbixAPI.hostgroup.get(output="extend")

def hostinterface():
    return ZabbixAPI.hostinterface.get(output="extend")

def hostprototype():
    return ZabbixAPI.hostprototype.get(output="extend")

def iconmap():
    return ZabbixAPI.iconmap.get(output="extend")

def image():
    return ZabbixAPI.image.get(output="extend")

def item():
    return ZabbixAPI.item.get(output="extend")

def itemprototype():
    return ZabbixAPI.itemprototype.get(output="extend")

def discoveryrule():
    return ZabbixAPI.discoveryrule.get(output="extend")

def maintenance():
    return ZabbixAPI.maintenance.get(output="extend")

def map():
    return ZabbixAPI.map.get(output="extend")

def mediatype():
    return ZabbixAPI.mediatype.get(output="extend")

def problem():
    return ZabbixAPI.problem.get(output="extend")

def proxy():
    return ZabbixAPI.proxy.get(output="extend")

def screen():
    return ZabbixAPI.screen.get(output="extend")

def screenitem():
    return ZabbixAPI.screenitem.get(output="extend")

def hostinterface():
    return ZabbixAPI.hostinterface.get(output="extend")

def script():
    return ZabbixAPI.script.get(output="extend")

def service():
    return ZabbixAPI.service.get(output="extend")

def template():
    return ZabbixAPI.template.get(output="extend")

def templatescreen():
    return ZabbixAPI.templatescreen.get(output="extend")

def trend():
    return ZabbixAPI.trend.get(output="extend")

def trigger():
    return ZabbixAPI.trigger.get(output="extend")

def triggerprototype():
    return ZabbixAPI.triggerprototype.get(output="extend")

def user():
    return ZabbixAPI.user.get(output="extend")

def usergroup():
    return ZabbixAPI.usergroup.get(output="extend")

def usermacro():
    return ZabbixAPI.usermacro.get(output="extend")

def valuemap():
    return ZabbixAPI.valuemap.get(output="extend")

def webscenario():
    return ZabbixAPI.webscenario.get(output="extend")

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

