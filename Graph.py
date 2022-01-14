import os
import time
import datetime
from pyzabbix import ZabbixAPI
from src.Utils import format_datetime
from src.Zabbix.API.Item import Item
from src.Zabbix.API.Server import Server
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates



os.system('cls')

ZAB_API = ZabbixAPI("http://guardiao.workdb.com.br/")
ZAB_API.login(user="lucas.hoeltgebaum", password="WorkDB#2021") # Preencha seu usuário e senha


if __name__ == "__main__":
    start_date = format_datetime("2022-01-01T00:00:00")
    end_date = format_datetime("2022-01-31T23:59:59")  
    host_id = 10306 # AUREA-DBSERVER
    graph_id = 6364
    server =  Server(ZAB_API, ZAB_API.host.get(output="extend", hostids=host_id)[0])
    graph = server.get_graphs(graph_id)[0]
    graph_items = graph.get_graph_items()
    items = server.get_items([g["itemid"] for g in graph_items])

    history = {item["name"]:item.get_history(start_date, end_date) for item in items}
    valores = []
    [valores := valores + v for k, v in history.items()]
    maior_valor = max([e['value'] for e in valores])
    menor_valor = min([e['value'] for e in valores])
    # variável logo acima contém os dados que serão utilizados para gerar o gráfico com id '6364'




plt.ylim(menor_valor, maior_valor)

datas = []
for i in range(21):
    new_time = start_date + datetime.timedelta( days = i )
    datas.append(new_time)

# plt.xticks(datas)

plt.xlim(datas[0], datas[1])

plt.title(graph['name'])


for item_name, history_list in history.items():
    values = {h['clock']:h['value'] for h in history_list}
    color = [g['color'] for g in graph_items if g['itemid'] == history_list[0]['itemid']][0]
    plt.plot(values.keys(), values.values(), label=item_name)

# plt.legend()

plt.show()
print('a')


figure.savefig('graph.png')



