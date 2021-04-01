#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Server import genServers, readServers, getAllServers
from pandas import read_excel
from os import system


class Zabbix():

    def __init__(self):
        self.servidores = []
        pass

    def readServers(self):
        self.servidores = readServers()
        print(self.servidores)

    def setServers(self, id = False):
        [self.servidores.append(servidor) for servidor in genServers(id = id)]

    def __searchServer(self, id):
        try:
            return [servidor for servidor in self.servidores if servidor.hostid == id][0]
        except IndexError:
            return "Servidor não encontrado"

    def serversToJSON(self, id = False):
        count = 0
        if not id:
            for serverObj in self.servidores:
                count += 1
                print(f"Saving {serverObj.host} to JSON {count}/{len(self.servidores)}.")
                serverObj.saveAll()
        else:
            serverObj = self.__searchServer(id)
            print(f"Saving {serverObj.host} to JSON.")
            serverObj.saveAll()

    def getItemValues(self, id = False):
        if not id:
            for serverObj in self.servidores:
                serverObj.getValues()
        else:
            serverObj = self.__searchServer(id)
            serverObj.getValues()

    def getServer(self, id = None, name = None):
        for server in self.servidores:
            if server.hostid == id:
                return server
            elif server.name == name:
                return server

    def gerarRelatorios(self, nome = False):
        if not nome:
            whitelist = []
            servidoresRelatorios = []
            data = read_excel("Relação Clientes Monitoramento Relatório.xlsx", sheet_name = "Clientes WorkDB")["Gerar Relatórios de"]
            for row in data:
                try:
                    [whitelist.append(server) for server in row.split(",")]
                except AttributeError:
                    pass
            for server in whitelist:
                try:
                    id = [servidor["hostid"] for servidor in getAllServers() if servidor["host"] == server][0]
                    self.setServers(id = id)
                    self.serversToJSON(id = id)
                    #self.getItemValues(id = id)
                    servidorObj = self.__searchServer(id)
                    servidorObj.gerarRelatorio()
                except IndexError:
                    print("\n\n")
                    print(f"Erro no nome {server}")
                    print("\n\n")
        else:
            id = [servidor["hostid"] for servidor in getAllServers() if servidor["host"] == nome.upper()][0]
            self.setServers(id = id)
            self.serversToJSON(id = id)
            servidorObj = self.__searchServer(id)
            servidorObj.gerarRelatorio()

def printMenu():
    print("1 - Gerar todos os relatórios")
    print("2 - Gerar relatório de servidor específico")
    opc = int(input())
    return opc

if __name__ == "__main__":
    zab = Zabbix()
    while True:
        opc = printMenu()
        if opc == 1:
            zab.gerarRelatorios()
        elif opc == 2:
            nome = input("Insira o nome do servidor\n")
            zab.gerarRelatorios(nome = nome)

        
    
    
    