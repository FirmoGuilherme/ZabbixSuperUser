from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject

class GraphItem(GenericZabbixObject):

    def __init__(self, raw_data):
        super().__init__(raw_data)
        """
            gitemid
            graphid
            itemid
            drawtype
            sortorder
            color
            yaxisside
            calc_fnc
            type
            max
            min
            average
        """