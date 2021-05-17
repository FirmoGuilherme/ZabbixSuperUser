from src.Utils import getZabbixAPI
ZabAPI = getZabbixAPI()

class GraphItem():

    def __init__(self, raw_data):
        try:
            for attribute in raw_data.keys():
                setattr(self, attribute, raw_data[attribute])
        except AttributeError: pass
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
        
    def historyFilter(self):
        self.allValues = []
        self.history = [hist for hist in ZabAPI.history.get(itemids = self.itemid, time_from=time_start, time_till=time_end, output='extend', limit='10000000')]
        if not len(self.history):
            self.history = [hist for hist in ZabAPI.history.get(itemids = self.itemid, time_from=time_start, time_till=time_end, output='extend', limit='10000000', history = 0)]
        if len(self.history) == 0: return False
        else:
            self.max = max([float(value["value"]) for value in self.history])
            self.min = min([float(value["value"]) for value in self.history])
            self.average = (sum([float(value["value"]) for value in self.history]) / len([float(value["value"]) for value in self.history]))
            return True
   