#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Server import Servidor
from json import load
from datetime import datetime
from pyzabbix import ZabbixAPI


class errorHandler(Exception):

    def __init__(self, error):
        with open("error.log", "a") as log:
            log.write(f"\n{datetime.now()}")
            log.write(error)
        if error == "auth.json not found":
            phrase = f"\n{datetime.now()}"
            phrase += "\nArquivo auth.json não encontrado!"
        super().__init__(phrase)
        
def readReq(classe):
    json_values = {}
    constructor_values = {}
    ## Extrai atributos necessários para instanciar a classe
    constructors = [constr for constr in classe.require]
    try:
        with open("auth.json", "r") as json:
            info = load(json)
            json_values["url"] = info["Website"]["url"]
            json_values["cookies"] = info["Website"]["cookies"]
            json_values["headers"] = info["Website"]["headers"]
            json_values["user"] = info["API"]["Username"]
            json_values["password"] = info["API"]["Password"]
            ## Adiciona valor necessário ao dicionário
            for const in constructors:
                constructor_values[const] = json_values[const]
        ## Instancia classe fornecida com devidos valores, baseando-se nos constructors da classe
        instance = classe(requirements = constructor_values)
        return instance
    except FileNotFoundError:
        raise errorHandler(error = "auth.json not found")


@readReq
class Zabbix():
    require = ["url", "user", "password"]

    def __init__(self, requirements = {}):
        self.API = ZabbixAPI(requirements["url"])
        self.API.login(requirements["user"], requirements["password"])
        self.readServers()
        #self.setServers()

    def readServers(self):
        self.servidores = []
        from os import listdir
        for server in listdir("Servers"):
            serverConfig, items, graphs, events = Servidor.readFromFile(server)
            self.servidores.append(Servidor(serverConfig, items, graphs, events))




    
    def setServers(self):
        self.servidores = []
        for servidor in self.API.host.get(output="extend"):
            print("Creating object %s"% servidor["host"])
            items = self.API.item.get(hostids = servidor["hostid"])
            graphs = self.API.graph.get(hostids = servidor["hostid"])
            events = self.API.event.get(hostids = servidor["hostid"])
            server = Servidor(servidor, items , graphs, events)
            self.servidores.append(server)

    def serversToJSON(self):
        for serverObj in self.servidores:
            serverObj.saveAll()

    def getServer(self, id = None, name = None):
        return [server for server in self.servidores if (server.hostid == id or server.name == name)][0]


if __name__ == "__main__":
    zab = Zabbix
    #zab.getServer(id = 10593)
    #zab.serversToJSON()