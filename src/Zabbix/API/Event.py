from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject

class Event(GenericZabbixObject):

    def __init__(self, raw_data):
        super().__init__(raw_data)