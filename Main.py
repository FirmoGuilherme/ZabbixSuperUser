#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from src.Server import genServers, readServers, getAllServers
from pandas import read_excel
from shutil import copyfile
from os import mkdir, listdir


def moverModelos():
    mkdir("ModelosNovos")
    for server in listdir("Servidores"):
        mkdir(r"ModelosNovos\{}".format(server))
        print(f"Movendo modelo {server}")
        try:
            copyfile(r"Servidores\{}\Graphs\_Model.docx".format(server), r"ModelosNovos\{}\_Model.docx".format(server))
        except FileNotFoundError:
            pass

class Zabbix():

    def __init__(self):
        self.servidores = {}

    def setServers(self, id = False):
        servidores = genServers(id = id)
        for servidor in servidores:
            self.servidores[servidor.host] = servidor

    def getServer(self, name):
        try:
            return self.servidores[name]
        except IndexError:
            return "Servidor não encontrado"

    def serversToJSON(self, name = False):
        count = 0
        if not name:
            for serverObj in self.servidores:
                count += 1
                print(f"Saving {serverObj.host} to JSON {count}/{len(self.servidores)}.")
                serverObj.saveAll()
        else:
            serverObj = self.getServer(name)
            print(f"Saving {serverObj.host} to JSON.")
            serverObj.saveAll()

    def getItemValues(self, id = False):
        if not id:
            for serverObj in self.servidores:
                serverObj.getValues()
        else:
            serverObj = self.getServer(id)
            serverObj.getValues()

    def gerarRelatorios(self, nome = False):
        if not nome:
            whitelist = []
            data = read_excel("Relação Clientes Monitoramento Relatório.xlsx", sheet_name = "Clientes WorkDB")["Gerar Relatórios de"]
            for row in data:
                try:
                    [whitelist.append(server) for server in row.split(",")]
                except AttributeError:
                    pass
            for server in whitelist:
                try:
                    id = [servidor["hostid"] for servidor in getAllServers() if servidor["host"] == server][0]
                    name = [servidor["host"] for servidor in getAllServers() if servidor["host"] == server][0]
                    self.setServers(id = id)
                    self.serversToJSON(name = name)
                    servidorObj = self.getServer(name)
                    servidorObj.gerarRelatorio()
                except IndexError:
                    print("\n\n")
                    print(f"Erro no nome {server}")
                    print("\n\n")
        else:
            id = [servidor["hostid"] for servidor in getAllServers() if servidor["host"] == nome.upper()][0]
            name = [servidor["host"] for servidor in getAllServers() if servidor["host"] == nome.upper()][0]
            self.setServers(id = id)
            self.serversToJSON(name = name)
            servidorObj = self.getServer(name)
            servidorObj.gerarRelatorio()

def printMenu():
    print("1 - Gerar todos os relatórios")
    print("2 - Gerar relatório de servidor específico")
    print("3 - Mover modelos para novo folder")
    opc = int(input())
    return opc

if __name__ == "__main__":
    zab = Zabbix()
    while True:
        opc = printMenu()
        if opc == 1:
            zab.gerarRelatorios()
        elif opc == 2:
            nome = input("Insira o nome do servidor\n").upper()
            zab.gerarRelatorios(nome = nome)
        elif opc == 3:
            moverModelos()