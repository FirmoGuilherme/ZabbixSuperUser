from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject
from io import BytesIO
from requests import get
from PIL.Image import open as read_bytes

class Graph(GenericZabbixObject):

    def __init__(self, raw_data):
        super().__init__(raw_data)

    def get_image(self):
        if "Disk" not in self.name and "Swap" not in self.name:
            self.image = self.__get_image_bytes(url = f"http://guardiao.workdb.com.br/chart2.php?graphid={self.graphid}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={self.graphid}=um5etv25&screenid=")
        else:
            self.image = self.__get_image_bytes(url = f"http://guardiao.workdb.com.br/chart2.php?graphid={self.graphid}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={self.graphid}&width=1274&height=280&_=um5ge3fh&screenid=")
        return self.image

    def __get_image_bytes(self, url):
        response = get(url, cookies=self.CONSTANTS.COOKIES, headers=self.CONSTANTS.HEADERS, verify=False)
        bytes = BytesIO(response.content)
        img = read_bytes(bytes)
        return img

    def get_graph_items(self):
        all_graphs = []
        graphs = CONSTANTS.ZABBIX_API.graphitem.get(graphids=self.graphid)
        for graph in graphs:
            all_graphs.append(GraphItem(graph))
        return all_graphs