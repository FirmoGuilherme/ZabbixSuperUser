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

class Server(GenericZabbixObject):

    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.events = []
        self.items = []
        self.graphs = []
        self.raw_data = raw_data
        
        t1 = Thread(target=self.__set_items)
        t1.start()
        t2 = Thread(target=self.__set_graphs)
        t2.start()
        t3 = Thread(target=self.__set_events)
        t3.start()
        t1.join(), t2.join(), t3.join()
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

    def __set_items(self):
        items = self.CONSTANTS.ZABBIX_API.item.get(hostids = self.hostid)
        for obj in items:
            self.items.append(Item(obj))

    def __set_graphs(self):
        graphs = self.CONSTANTS.ZABBIX_API.graph.get(hostids = self.hostid)
        for obj in graphs:
            self.graphs.append(Graph(obj))

    def __set_events(self):
        events = self.CONSTANTS.ZABBIX_API.event.get(hostids = self.hostid)
        for obj in events:
            self.events.append(Event(obj))

    def gerar_relatorio(self):
        '''
        0 = Modelo encontrado
        1 = Modelo não encontrado
        '''
        path_salvar = path.join(self.CONSTANTS.CONFIGS.relatorios_storage, self.host)
        try:
            makedirs(path_salvar)
        except FileExistsError:
            pass
        try:
            copy(path.join(self.CONSTANTS.CONFIGS.modelos_storage, f"{self.host}.docx"), 
                path.join(path_salvar, f"_{self.host}.docx"))
        except FileExistsError:
            # Modelo ja no folder do servidor
            remove(path.join(self.CONSTANTS.CONFIGS.modelos_storage, f"{self.host}.docx"))
            copy(path.join(self.CONSTANTS.CONFIGS.modelos_storage, f"{self.host}.docx"), 
                path.join(path_salvar, f"_{self.host}.docx"))
        except FileNotFoundError:
            # Sem modelo
            pass

        for graph in self.graphs:
            img = graph.get_image()
            img.save(path.join(path_salvar, f"{graph.name}.png"))
