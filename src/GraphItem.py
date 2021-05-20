from src.Utils import ZabbixAPI, datetime
from time import mktime

time_end = int(mktime(datetime.now().timetuple()))
time_start = time_end - 60 * 60 * 24 * 31

class GraphItem():

    def __init__(self, raw_data):
        try:
            for attribute in raw_data.keys():
                setattr(self, attribute, raw_data[attribute])
        except AttributeError: pass
        print(self.__dict__)
        self.getHistory()
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
        
    def getHistory(self):

        self.history = ZabbixAPI.history.get(itemids=self.itemid, time_start=time_statr, time_end=time_end)
   