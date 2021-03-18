#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Server import Servidor
from Utils import getZabbixAPI


class Zabbix():

    def __init__(self):
        self.API = None


    def readServers(self):
        self.servidores = []
        from os import listdir
        for server in listdir("Servers"):
            print(f"Reading object {server}")
            serverConfig, items, graphs, events = Servidor.readFromFile(server)
            self.servidores.append(Servidor(serverConfig, items, graphs, events))


    def setServers(self):
        self.API = getZabbixAPI()
        self.servidores = []
        for servidor in self.API.host.get(output="extend"):
            print("Creating object %s"% servidor["host"])
            items = self.API.item.get(hostids = servidor["hostid"])
            graphs = self.API.graph.get(hostids = servidor["hostid"])
            events = self.API.event.get(hostids = servidor["hostid"])
            server = Servidor(servidor, items , graphs, events)
            self.servidores.append(server)

    def setSingleServer(self, id):
        self.API = getZabbixAPI()
        self.servidores = []
        for servidor in self.API.host.get(hostids=id, output="extend"):
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
        for server in self.servidores:
            if server.hostid == id:
                return server
            elif server.name == name:
                return server


if __name__ == "__main__":
    zab = Zabbix()
    #zab.readServers()
    #zab.setServers()
    zab.setSingleServer(10634)
    zab.serversToJSON()
    