from src.Utils import getImage, ZabbixAPI


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
            try:
                if raw_data[attribute].isnumeric():
                    self.__translateNumeric(attribute, raw_data[attribute])
            except AttributeError: pass
        
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

        if "Disk" not in self.name and "Swap" not in self.name:
            self.image = getImage(url = "http://guardiao.workdb.com.br/chart2.php?graphid={}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={}=um5etv25&screenid=".format(self.graphid, self.graphid))
        else:
            self.image = getImage(url = "http://guardiao.workdb.com.br/chart2.php?graphid={}&from=now-1M%2FM&to=now-1M%2FM&profileIdx=web.graphs.filter&profileIdx2={}&width=1274&height=280&_=um5ge3fh&screenid=".format(self.graphid, self.graphid))
        return self.image

    def getItems(self):
        return ZabbixAPI.graphitem.get(graphids = self.graphid)

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
        try: setattr(self, attribute, translations[attribute][int(value)])
        except KeyError: pass