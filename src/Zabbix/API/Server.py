from shutil import copy
from json import dump
from os import path, makedirs, remove
from threading import Thread

## Custom Imports
from src.Zabbix.API.Event import Event
from src.Zabbix.API.Item import Item
from src.Zabbix.API.GraphItem import GraphItem
from src.Zabbix.API.Graph import Graph
from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject
from src.Constants.Constants import CONSTANTS



class Server(GenericZabbixObject):

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

    def __post_init__(self):
        t1 = Thread(target=self.__set_items)
        t1.start()
        t2 = Thread(target=self.__set_graphs)
        t2.start()
        t3 = Thread(target=self.__set_events)
        t3.start()
        t1.join(), t2.join(), t3.join()

    def __set_items(self):
        items = self.api.item.get(hostids = self['hostid'])
        self.items = [Item(self.api, data) for data in items]

    def __set_graphs(self):
        graphs = self.api.graph.get(hostids = self['hostid'])
        self.graphs = [Graph(self.api, data) for data in graphs]

    def __set_events(self):
        events = self.api.event.get(hostids = self['hostid'])
        self.events = [Event(self.api, data) for data in events]

    def get_graphs(self, ids: str or int or float or list[str or int or float]) -> list[Item]:
        ids = [int(ids)] if type(ids) in (str, int, float) else [int(i) for i in ids]
        return [i for i in self.graphs if i["graphid"] in ids]

    def get_items(self, ids: str or int or float or list[str or int or float]) -> list[Item]:
        ids = [int(ids)] if type(ids) in (str, int, float) else [int(i) for i in ids]
        return [i for i in self.items if i["itemid"] in ids]

    def gerar_relatorio(self, start_date, end_date) -> (Exception, str):
        error = None
        path_salvar = path.join(CONSTANTS.CONFIGS.relatorios_storage, self["host"])
        try:
            makedirs(path_salvar)
        except FileExistsError:
            pass

        try:
            copy(path.join(CONSTANTS.CONFIGS.modelos_storage, f"{self['host']}.docx"), 
                path.join(path_salvar, f"_{self['host']}.docx"))
        except FileExistsError:
            # Modelo ja no folder do servidor
            remove(path.join(CONSTANTS.CONFIGS.modelos_storage, f"{self['host']}.docx"))
            copy(path.join(CONSTANTS.CONFIGS.modelos_storage, f"{self['host']}.docx"), 
                path.join(path_salvar, f"_{self['host']}.docx"))
        except FileNotFoundError as error:
            pass

        for graph in self.graphs:
            img = graph.get_image(start_date, end_date)
            img.save(path.join(path_salvar, f"{graph['name']}.png"))

        return error, self["host"]