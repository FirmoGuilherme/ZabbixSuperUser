#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Server import genServers


class Zabbix():

    def __init__(self):
        pass

    def readServers(self):
        self.servidores = []
        from os import listdir
        for server in listdir("Servers"):
            print(f"Reading object {server}")
            serverConfig, items, graphs, events = Servidor.readFromFile(server)
            self.servidores.append(Servidor(serverConfig, items, graphs, events))

    def setServers(self, id = False):
        self.servidores = genServers(id = id)

    def serversToJSON(self):
        for serverObj in self.servidores:
            serverObj.saveAll()

    def getItemValues(self):
        for serverObj in self.servidores:
            serverObj.getValues()

    def getServer(self, id = None, name = None):
        for server in self.servidores:
            if server.hostid == id:
                return server
            elif server.name == name:
                return server


if __name__ == "__main__":
    zab = Zabbix()
    zab.setServers(10084)
    zab.getItemValues()
    