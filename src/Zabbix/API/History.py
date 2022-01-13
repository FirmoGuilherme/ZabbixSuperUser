import datetime
from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject

class History(GenericZabbixObject):

    def __post_init__(self):
        self['value'] = float(self['value']) if type(self['value']) is str else self['value']
        self['clock'] = datetime.datetime.fromtimestamp(self['clock'])