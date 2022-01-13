from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject
from src.Constants.Constants import CONSTANTS
from .GraphItem import GraphItem
from io import BytesIO
import requests
from PIL.Image import open as read_bytes

class Graph(GenericZabbixObject):
    
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

    def __init__(self, api, raw_data):
        super().__init__(api, raw_data)

    def get_image(self, start_date, end_date):
        if "Disk" not in self['name'] and "Swap" not in self['name']:
            self.image = self.__get_image_bytes(url = f'http://guardiao.workdb.com.br/chart2.php?graphid={self["graphid"]}&from={start_date}&to={end_date}&profileIdx=web.graphs.filter&profileIdx2={self["graphid"]}=um5etv25&screenid=')
        else:
            self.image = self.__get_image_bytes(url = f'http://guardiao.workdb.com.br/chart2.php?graphid={self["graphid"]}&from={start_date}&to={end_date}&profileIdx=web.graphs.filter&profileIdx2={self["graphid"]}&width=1274&height=280&_=um5ge3fh&screenid=')
        return self.image

    def __get_image_bytes(self, url):
        response = requests.get(url, cookies=CONSTANTS.COOKIES, headers=CONSTANTS.HEADERS, verify=False)
        bytes = BytesIO(response.content)
        return read_bytes(bytes)

    def get_graph_items(self):
        graphs = self.api.graphitem.get(graphids=self["graphid"])
        return [GraphItem(self.api, graph) for graph in graphs]