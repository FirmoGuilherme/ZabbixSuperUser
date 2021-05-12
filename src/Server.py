from shutil import copy
from json import dump
from os import listdir

## Custom Imports
from src.Utils import getZabbixAPI, removeInvalidChar, getSessID, toJSON, getDate, translateBytes, loadJson
from src.Event import Event
from src.Item import Item
from src.GraphItem import GraphItem
from src.Graph import Graph



ZabAPI = getZabbixAPI()
zabbixSessionID, phpSessionID = getSessID()
time_start, time_end = getDate()


class Servidor():

    def __init__(self, raw_data, items, graphs, events):
        blacklist = [
            "hostid",
            "proxy_hostid",
            "disable_until",
            "errors_from",
            "lastaccess",
            "ipmi_disable_until",
            "snmp_disable_until",
            "maintenanceid",
            "maintenance_from",
            "ipmi_errors_from",
            "snmp_errors_from",
            "jmx_disable_until",
            "jmx_available",
            "jmx_errors_from",
            "templateid",
            "tls_connect",
            "auto_compress"
        ]
        self.raw_data = raw_data
        for attribute in raw_data.keys():
            setattr(self, attribute, raw_data[attribute])
            if attribute not in blacklist and raw_data[attribute].isnumeric():
                self.__translateNumeric(attribute, raw_data[attribute])
        self.__setItems(items)
        self.__setGraphs(graphs)
        self.__setEvents(events)
        self.__filterInnactive()
        """
            hostid
            proxy_hostid
            host
            status
            disable_until
            error
            available
            errors_from
            lastaccess
            ipmi_authtype
            ipmi_privilege
            ipmi_username
            ipmi_password
            ipmi_disable_until
            ipmi_available
            snmp_disable_until
            snmp_available
            maintenanceid
            maintenance_status
            maintenance_type
            maintenance_from
            ipmi_errors_from
            snmp_errors_from
            ipmi_error
            snmp_error
            jmx_disable_until
            jmx_available
            jmx_errors_from
            jmx_error
            name
            flags
            templateid
            description
            tls_connect
            tls_accept
            tls_issuer
            tls_subject
            tls_psk_identity
            tls_psk
            proxy_address
            auto_compress
            inventory_mode
         """

    def __translateNumeric(self , attribute, value):
        translations = {
            "available":{
                0: "(default) unknow",
                1: "available",
                2: "unavailable"
            },
            "flags":{
                0: "a plain host",
                4: "a discovered host"
            },
            "inventory_mode":{
               -1: "disabled",
                0: "(default) normal",
                1: "automatic"
            },
            "ipmi_authtype":{
               -1: "(default) default",
                0: "none",
                1: "MD2",
                2: "MD5",
                4: "straight",
                5: "OEM",
                6: "RMCP+"
            },
            "ipmi_available":{
                0: "(default) unknow",
                1: "available",
                2: "unavailable"
            },
            "ipmi_privilege":{
                1: "callback",
                2: "(default) user",
                3: "operator",
                4: "admin",
                5: "OEM"
            },
            "jxm_available":{
                0: "(default) unknow",
                1: "available",
                2: "unavailable"
            },
            "maintenance_status":{
                0: "(default) no maintenance",
                1: "maintenance in effect"
            },
            "maintenance_type":{
                0: "(default) maintenance with data collection",
                1: "maintenance without data collection"
            },
            "snmp_available":{
                0: "(default) unkown",
                1: "available",
                2: "unavailable"
            },
            "status":{
                0: "(default) No encryption",
                1: "unmonitored host"
            },
            "tls_connect":{
                0: "(default) No encryption",
                1: "PSK",
                4: "certificate"
            },
            "tls_accept":{
                1: "(default) No encryption",
                2: "PSK",
                4: "certificate"
            }
        }
        setattr(self, attribute, translations[attribute][int(value)])

    def __setEvents(self, events):
        self.events = {}
        for event in events:
            eventObj = Event(event)
            self.events[eventObj.name] = eventObj

    def __setItems(self, items):
        self.items = {}
        for item in items:
            itemObj = Item(item)
            self.items[itemObj.name] = itemObj

    def __setGraphs(self, graphs):
        self.graphs = {}
        for rawData in graphs:
            graphObj = Graph(rawData)
            self.graphs[graphObj.name] = graphObj

    def __filterInnactive(self):
        self.itemsInactive = [item for item in self.items.values() if (item.state == "not supported" or item.status == "disabled item")]
        self.itemsActive = [item for item in self.items.values() if (item.state != "not supported" or item.status != "disabled item")]

    def getValues(self):
        self.graphItem = {}
        for graph in self.graphs.values():
            mydict = {}
            name = removeInvalidChar(graph.name)
            graphItems = graph.getItems()
            for item in graphItems:
                graphItemOBJ = GraphItem(item)
                hasHistory = graphItemOBJ.historyFilter()
                if hasHistory:
                    try:
                        itemName = [item.name for item in self.items if item.itemid == graphItemOBJ.itemid][0]
                        graphItemOBJ.allValues, graphItemOBJ.max, graphItemOBJ.min, graphItemOBJ.average = translateBytes(graphItemOBJ, itemName)
                        if graphItemOBJ.graphid not in self.graphItem.keys():
                            self.graphItem[graphItemOBJ.graphid] = [graphItemOBJ]
                        else:
                            self.graphItem[graphItemOBJ.graphid].append(graphItemOBJ)
                        mydict[itemName] = {}
                        for att, value in zip(graphItemOBJ.__dict__, graphItemOBJ.__dict__.values()):
                            mydict[itemName][att] = value
                    except IndexError: pass
            with open(f"Servidores\{self.host}\Graphs\{name} - Values.json", "w") as json:
                dump(mydict, json, indent=4)
                    
    def saveAll(self):
        from os import makedirs
        try: makedirs(f"Servidores\\{self.host}\\Items\\Enabled")
        except FileExistsError: pass
        try: makedirs(f"Servidores\\{self.host}\\Items\\Disabled\\unSupported")
        except FileExistsError: pass
        try: makedirs(f"Servidores\\{self.host}\\Graphs")
        except FileExistsError: pass
        try: makedirs(f"Servidores\\{self.host}\\Events")
        except FileExistsError: pass

        ## Server Config
        toJSON(self.__dict__, self.__dict__.values(), f"Servidores\{self.host}\config.json")

        def items():
            for item in self.items.values():
                name = removeInvalidChar(item.name)
                if item.state == "not supported":
                    toJSON(item.__dict__, item.__dict__.values(), f"Servidores\\{self.host}\\Items\\Disabled\\unSupported\\{name}.json")
                elif item.status == "disabled item":
                    toJSON(item.__dict__, item.__dict__.values(), f"Servidores\\{self.host}\\Items\\Disabled\\{name}.json")
                else:
                    toJSON(item.__dict__, item.__dict__.values(), f"Servidores\\{self.host}\\Items\\Enabled\\{name}.json")

        def graphs():
            for graph in self.graphs.values():
                name = removeInvalidChar(graph.name)
                img = graph.getGraphImage()
                img.save(f"Servidores\{self.host}\Graphs\{name}.png")
                toJSON(graph.__dict__, graph.__dict__.values(), f"Servidores\{self.host}\Graphs\{name}.json")

        def events():
            for event in self.events.values():
                name = removeInvalidChar(event.name)
                toJSON(event.__dict__, event.__dict__.values(), f"Servidores\{self.host}\Events\{name}.json")

        items()
        graphs()
        events()
    
    def gerarRelatorio(self):
        try:
            copy(f"Modelos/{self.host}/_{self.host}.docx", f"Servidores/{self.host}/Graphs/_{self.host}.docx")
        except FileNotFoundError:
            print("\n\n")
            print(f"Arquivo modelo {self.host} não encontrado!")
            print("\n\n")


def readFromFile(nome):
    from json import load
    from os import listdir
    serverConfig = {}
    items = []
    graphs = []
    events = []
    with open(f"Servidores\{nome}\config.json", "r") as Config:
        data = load(Config)
        for attribute, value in zip(data.keys(), data.values()):
            serverConfig[attribute] = value


    ## Items não suportados
    for item in listdir(f"Servidores\\{nome}\\Items\\Disabled\\unSupported"): 
        items.append(loadJson(f"Servidores\\{nome}\\Items\\Disabled\\unSupported\\{item}"))
    ## Items desabilitados
    for item in [item for item in listdir(f"Servidores\{nome}\Items\Disabled") if item != "unSupported"]: 
        items.append(loadJson(f"Servidores\{nome}\Items\Disabled\{item}"))
    ## Items habilitados
    for item in listdir(f"Servidores\{nome}\Items\Enabled"): 
        items.append(loadJson(f"Servidores\{nome}\Items\Enabled\{item}"))


    ## Gráficos
    for graph in [graph for graph in listdir(f"Servidores\{nome}\Graphs") if graph.endswith("json") and "Values" not in graph]:
        graphs.append(loadJson(f"Servidores\{nome}\Graphs\{graph}"))


    ## Eventos
    for event in listdir(f"Servidores\{nome}\Events"): 
        events.append(loadJson(f"Servidores\{nome}\Events\{event}"))

    return serverConfig, items, graphs, events




def genServers(id):
    servidores = []
    if not id: 
        for servidor in ZabAPI.host.get(output="extend"):
            print("Creating object %s"% servidor["host"])
            items = ZabAPI.item.get(hostids = servidor["hostid"])
            graphs = ZabAPI.graph.get(hostids = servidor["hostid"])
            events = ZabAPI.event.get(hostids = servidor["hostid"])
            server = Servidor(servidor, items , graphs, events)
            servidores.append(server)
    else:
        servidor = ZabAPI.host.get(hostids=id, output="extend")[0]
        print("Creating object %s"% servidor["host"])
        items = ZabAPI.item.get(hostids = servidor["hostid"])
        graphs = ZabAPI.graph.get(hostids = servidor["hostid"])
        events = ZabAPI.event.get(hostids = servidor["hostid"])
        server = Servidor(servidor, items , graphs, events)
        servidores.append(server)
    return servidores


def getAllServers():
    return [servidor for servidor in ZabAPI.host.get(output="extend")]

def readServers():
    servidores = []
    try:
        for server in listdir("Servidores"):
            print(f"Reading object {server}")
            serverConfig, items, graphs, events = readFromFile(server)
            serv = Servidor(serverConfig, items, graphs, events)
            servidores.append(serv)
    except FileNotFoundError: pass
    return servidores
