from Utils import getZabbixAPI, removeInvalidChar, getImage, getBar, getSessID, toJSON
from time import mktime
from json import dump
from datetime import datetime

ZabAPI = getZabbixAPI()
zabbixSessionID, phpSessionID = getSessID()
time_end = int(mktime(datetime.now().timetuple()))
time_start = time_end - 60 * 60 * 24 * 31


class Item():

    def __init__(self, raw_data):
        blacklist = [
            "itemid",
            "hostid",
            "trends",
            "history",
            "templateid",
            "valuemapid",
            "interfaceid",
            "inventory_link",
            "evaltype",
            "master_itemid",
            "query_fields",
            "status_codes",
            "headers",
            "lastclock",
            "lastns",
            "lifetime",
            "lastvalue",
            "prevvalue",
            "delay"
            ]
        for attribute in raw_data.keys():
            setattr(self, attribute, raw_data[attribute])
            if attribute not in blacklist and raw_data[attribute].isnumeric():
                self.__translateNumeric(attribute, raw_data[attribute])
        """
            itemid
            type
            snmp_community
            snmp_oid
            hostid
            name
            key_
            delay
            history
            trends
            status
            value_type
            trapper_hosts
            units
            snmpv3_securityname
            snmpv3_securitylevel
            snmpv3_authpassphrase
            snmpv3_privpassphrase
            formula
            logtimefmt
            templateid
            valuemapid
            params
            ipmi_sensor
            authtype
            username
            password
            publickey
            privatekey
            flags
            interfaceid
            port
            description
            inventory_link
            lifetime
            snmpv3_authprotocol
            snmpv3_privprotocol
            snmpv3_contextname
            evaltype
            jmx_endpoint
            master_itemid
            timeout
            url
            query_fields
            posts
            status_codes
            follow_redirects
            post_type
            http_proxy
            headers
            retrieve_mode
            request_method
            output_format
            ssl_cert_file
            ssl_key_file
            ssl_key_password
            verify_peer
            verify_host
            allow_traps
            state
            error
            lastclock
            lastns
            lastvalue
            prevvalue
        """
        if self.flags == "a discovered item":
            self.setName()

    def setName(self):
        ## Disk discovery
        if "vfs" in self.key_:
            self.name = self.name.replace("$1", self.key_.split("[")[1].split(",")[0])

        ## Network Interface Discovery
        elif "net" in self.key_:
            self.name = self.name.replace("$1", self.key_.split("[")[1][0:-1])

        ## Oracle Tablespace Discovery
        elif "oracle" in self.key_:
            self.name = self.name[0:-7]
        

    def __translateNumeric(self , attribute, value):
        translations = {
            "type":{
                0: "Zabbix agent",
                1: "SNMPv1 agent",
                2: "Zabbix trapper",
                3: "simple check",
                4: "SNMPv2 agent",
                5: "Zabbix internal",
                6: "SNMPv3 agent",
                7: "Zabbix agent (active)",
                8: "Zabbix aggregate",
                9: "web item",
                10: "external check",
                11: "database monitor",
                12: "IPMI agent",
                13: "SSH agent",
                14: "TELNET agent",
                15: "calculated",
                16: "JMX agent",
                17: "SNMP trap",
                18: "Dependent item",
                19: "HTTP agent", 
            },
            "value_type":{
                0: "numeric float",
                1: "character",
                2: "log",
                3: "numeric unsigned",
                4: "text"
            },
            "allow_traps":{
                0: "(default) Do not allow to accept incoming data",
                1: "Allow to accept incoming data"
            },
            "authtype":{
                0: "(default) none",
                1: "basic",
                2: "NTLM"
            },
            "flags":{
                0: "a plain item",
                4: "a discovered item"
            },
            "follow_redirects":{
                0: "Do not follow redirects",
                1: "(default) Follow redirects"
            },
            "output_format":{
                0: "(default) Store raw",
                1: "Convert to JSON"
            },
            "post_type":{
                0: "(default) Raw data",
                2: "JSON data",
                3: "XML data"
            },
            "request_method":{
                0: "(default) set",
                1: "POST",
                2: "PUT",
                3: "HEAD"
            },
            "retrieve_mode":{
                0: "(default) Body",
                1: "Headers",
                2: "Both body and headers will be stored"
            },
            "snmpv3_authprotocol":{
                0: "(default) MD5",
                1: "SHA"
            },
            "snmpv3_privprotocol":{
                0: "(default) DES",
                1: "AES"
            },
            "snmpv3_securitylevel":{
                0: "noAuthNoPriv",
                1: "atuHnoPriv",
                2: "authPriv"
            },
            "state":{
                0: "(default) normal",
                1: "not supported"
            },
            "status":{
                0: "(default) enabled item",
                1: "disabled item"
            },
            "verify_host":{
                0: "(default) Do not validate",
                1: "Validate"
            },
            "verify_peer":{
                0: "(default) Do not validate",
                1: "Validate"
            }
        }
        setattr(self, attribute, translations[attribute][int(value)])

class Graph():

    def __init__(self, raw_data):
        blacklist = [
            "graphid",
            "width",
            "height",
            "templateid",
            "ymin_itemid",
            "ymax_itemid",
            ]
        for attribute in raw_data.keys():
            setattr(self, attribute, raw_data[attribute])
            if attribute not in blacklist and raw_data[attribute].isnumeric():
                self.__translateNumeric(attribute, raw_data[attribute])
        
        """
            graphid
            name
            width
            height
            yaxismin
            yaxismax
            templateid
            show_work_period
            show_triggers
            graphtype
            show_legend
            show_3d
            percent_left
            percent_right
            ymin_type
            ymax_type
            ymin_itemid
            ymax_itemid
            flags
        """

    def getGraphImage(self):
        self.image = getImage(url = "http://guardiao.workdb.com.br/chart2.php?graphid={}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={}=um5etv25&screenid=".format(self.graphid, self.graphid),zbxsessID=zabbixSessionID, phpsessID = phpSessionID )
        return self.image

    def getItems(self):
        return ZabAPI.graphitem.get(graphids = self.graphid)

    def __translateNumeric(self , attribute, value):
        translations = {
            "flags":{
                0: "(default) a plain graph",
                4: "a discovered graph"
            },
            "graphtype":{
                0: "(default) normal)",
                1: "stacked",
                2: "pie",
                3: "exploded",
            },
            "show_3d":{
                0: "(default) show in 2D",
                1: "show in 3d",
            },
            "show_legend":{
                0: "hide",
                1: "(default) show"
            },
            "show_work_period":{
                0: "hide",
                1: "(default) show",
                2: "NTLM"
            },
            "show_triggers":{
                0: "hide",
                1: "(default) show"
            },
            "ymax_type":{
                0: "(default) calculated",
                1: "fixed",
                2: "item"
            },
            "ymin_type":{
                0: "(default) calculated",
                1: "fixed",
                2: "item"
            }
        }
        setattr(self, attribute, translations[attribute][int(value)])

class GraphItem():

    def __init__(self, raw_data):
        for attribute in raw_data.keys():
            setattr(self, attribute, raw_data[attribute])
        

    def historyFilter(self):
        history = [int(hist["value"]) for hist in ZabAPI.history.get(itemids = self.itemid, time_from=time_start, time_till=time_end, output='extend', limit='10000000') if len(hist) > 0]
        if self.itemid == "34273":
            print(history)
        if len(history) == 0: return False
        else:
            self.max = max(history)
            self.min = min(history)
            self.average = (sum(history) / len(history))
            return True
        
class Event():

    def __init__(self, raw_data):
        blacklist = [
            "eventid",
            "objectid",
            "clock",
            "ns",
            "r_eventid",
            "correlationid",
            "userid",
            "urls",
            "acknowledged",
            "c_eventid",
            ]
        self.raw_data = raw_data
        for attribute in raw_data.keys():
            setattr(self, attribute, raw_data[attribute])
            if attribute not in blacklist and raw_data[attribute].isnumeric():
                self.__translateNumeric(attribute, raw_data[attribute])
        """
            eventid
            source
            object
            objectid
            clock
            value
            acknowledge
            ns
            name
            severity
            4_eventid
            c_eventid
            correlationid
            userid
            opdata
            supressed
            urls
        """

    def __translateNumeric(self , attribute, value):
        translations = {
            "source":{
                0: "event created by a trigger",
                1: "event created by a discovery rule",
                2: "event created by active agent auto-registration",
                3: "internal event",
            },
            "object":{
                0: "trigger",
                1: "discovered host",
                2: "discovered service",
                3: "auto-registered host",
                4: "item",
                5: "LLD rule"
            },
            "value":{
                0: "OK",
                1: "problem / host or service down / unknown or not supported state",
                2: "host or service discovered",
                3: "host or service lost"
            },
            "severity":{
                0: "not classified",
                1: "information",
                2: "warning",
                3: "average",
                4: "high",
                5: "disaster"
            },
            "suppressed":{
                0: "event is in normal state",
                1: "event is supressed"
            }
        }
        setattr(self, attribute, translations[attribute][int(value)])


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
        self.events = []
        for event in events:
            self.events.append(Event(event))

    def __setItems(self, items):
        self.items = []
        for item in items:
            self.items.append(Item(item))

    def __setGraphs(self, graphs):
        self.graphs = []
        for rawData in graphs:
            graphObj = Graph(rawData)
            self.graphs.append(graphObj)

    def __filterInnactive(self):
        self.itemsInactive = [item for item in self.items if (item.state == "not supported" or item.status == "disabled item")]
        self.itemsActive = [item for item in self.items if (item.state != "not supported" or item.status != "disabled item")]

    def getValues(self):
        barra = getBar()
        for graph in self.graphs:
            mydict = {}
            name = removeInvalidChar(graph.name)
            graphItems = graph.getItems()
            for item in graphItems:
                graphItemOBJ = GraphItem(item)
                hasHistory = graphItemOBJ.historyFilter()
                if hasHistory:
                    itemName = [item.name for item in self.items if item.itemid == graphItemOBJ.itemid][0]
                    mydict[itemName] = {}
                    for att, value in zip(graphItemOBJ.__dict__, graphItemOBJ.__dict__.values()):
                         mydict[itemName][att] = value
            with open(f"Servers{barra}{self.host}{barra}Graphs{barra}{name} - Values.json", "w") as json:
                dump(mydict, json, indent=4)
                    
    def saveAll(self):
        from os import makedirs
        barra = getBar()
        try: makedirs(f"Servers{barra}{self.host}{barra}Items{barra}Enabled")
        except FileExistsError: pass
        try: makedirs(f"Servers{barra}{self.host}{barra}Items{barra}Disabled{barra}unSupported")
        except FileExistsError: pass
        try: makedirs(f"Servers{barra}{self.host}{barra}Graphs")
        except FileExistsError: pass
        try: makedirs(f"Servers{barra}{self.host}{barra}Events")
        except FileExistsError: pass

        ## Server Config
        toJSON(self.__dict__, self.__dict__.values(), f"Servers{barra}{self.host}{barra}config.json")

        def items():
            for item in self.items:
                name = removeInvalidChar(item.name)
                if item.state == "not supported":
                    toJSON(item.__dict__, item.__dict__.values(), f"Servers{barra}{self.host}{barra}Items{barra}Disabled{barra}unSupported{barra}{name}.json")
                elif item.status == "disabled item":
                    toJSON(item.__dict__, item.__dict__.values(), f"Servers{barra}{self.host}{barra}Items{barra}Disabled{barra}{name}.json")
                else:
                    toJSON(item.__dict__, item.__dict__.values(), f"Servers{barra}{self.host}{barra}Items{barra}Enabled{barra}{name}.json")

        def graphs():
            for graph in self.graphs:
                name = removeInvalidChar(graph.name)
                img = graph.getGraphImage()
                img.save(f"Servers{barra}{self.host}{barra}Graphs{barra}{name}.png")
                toJSON(graph.__dict__, graph.__dict__.values(), f"Servers{barra}{self.host}{barra}Graphs{barra}{name}.json")

        def events():
            for event in self.events:
                name = removeInvalidChar(event.name)
                toJSON(event.__dict__, event.__dict__.values(), f"Servers{barra}{self.host}{barra}Events{barra}{name}.json")

        items()
        graphs()
        events()

    def readFromFile(nome):
        from json import load
        from os import listdir
        barra = getBar()
        serverConfig = {}
        items = []
        graphs = []
        events = []
        with open(f"Servers{barra}{nome}{barra}config.json", "r") as Config:
            data = load(Config)
            for attribute, value in zip(data.keys(), data.values()):
                serverConfig[attribute] = value
        ## Items não suportados
        for item in listdir(f"Servers{barra}{nome}{barra}Items{barra}Disabled{barra}unSupported"): 
            with open(f"Servers{barra}{nome}{barra}Items{barra}Disabled{barra}unSupported{barra}{item}", "r") as json:
                data = load(json)
            items.append(data)
        ## Items desabilitados
        for item in listdir(f"Servers{barra}{nome}{barra}Items{barra}Disabled"): 
            if item != "unSupported":
                with open(f"Servers{barra}{nome}{barra}Items{barra}Disabled{barra}{item}", "r") as json:
                    data = load(json)
                items.append(data)
        ## Items habilitados
        for item in listdir(f"Servers{barra}{nome}{barra}Items{barra}Enabled"): 
            with open(f"Servers{barra}{nome}{barra}Items{barra}Enabled{barra}{item}", "r") as json:
                data = load(json)
            items.append(data)

        ## Gráficos
        for graph in listdir(f"Servers{barra}{nome}{barra}Graphs"): 
            with open(f"Servers{barra}{nome}{barra}Graphs{barra}{graph}", "r") as json:
                data = load(json)
            graphs.append(data)

        ## Eventos
        for event in listdir(f"Servers{barra}{nome}{barra}Events"): 
            with open(f"Servers{barra}{nome}{barra}Events{barra}{event}", "r") as json:
                data = load(json)
            events.append(data)

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
        for servidor in ZabAPI.host.get(hostids=id, output="extend"):
            print("Creating object %s"% servidor["host"])
            items = ZabAPI.item.get(hostids = servidor["hostid"])
            graphs = ZabAPI.graph.get(hostids = servidor["hostid"])
            events = ZabAPI.event.get(hostids = servidor["hostid"])
            server = Servidor(servidor, items , graphs, events)
            servidores.append(server)
    return servidores

