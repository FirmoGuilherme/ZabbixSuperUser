#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from src.Server import genServers, getAllServers, readServers
from src.Utils import errorLog
from pandas import read_excel
from shutil import copyfile
from os import mkdir, listdir, system

errors = {}
def moverModelos():
    system("cls")
    try: mkdir("ModelosNovos")
    except FileExistsError: pass
    for server in listdir("Servidores"):
        try: mkdir(r"ModelosNovos\{}".format(server))
        except FileExistsError: pass
        try:
            copyfile(r"Servidores\{}\Graphs\{}".format(server, [file for file in listdir(r"Servidores\{}\Graphs".format(server)) if file.endswith("docx")][0]), r"ModelosNovos\{}\_{}.docx".format(server, server))
        except IndexError: errors[server] = f"Modelo não encontrado na pasta de Servidores!"
    print("\n")
    print("Selecione TODOS os arquivos na pasta 'ModelosNovos'\nE coloque-os na pasta 'Modelos'")

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
                serverObj.saveAll()
        else:
            serverObj = self.getServer(name)
            serverObj.saveAll()

    def getItemValues(self, id = False):
        if not id:
            for serverObj in self.servidores:
                serverObj.getValues()
        else:
            serverObj = self.getServer(id)
            serverObj.getValues()

    def readFromFile(self):
        servidores = readServers()
        for server in servidores:
            self.servidores[server.host] = server

    def gerarRelatorios(self, nome = False):
        if not nome:
            whitelist = []
            try:
                data = read_excel("Relação Clientes Monitoramento Relatório.xlsx", sheet_name = "Clientes WorkDB")["Gerar Relatórios de"]
            except FileNotFoundError as excp:
                errorLog(excp, "Arquivo com relação de servidores não encontrado!\nCrie o arquivo 'Relação Clientes Monitoramento Relatório.xlsx' na mesma pasta que o programa\nCrie então uma coluna com o nome 'Clientes WorkDB' e, abaixo dela, adicione os servidores que devem ser gerados relatórios", writeTraceback = True, raiseError = True)
            except ValueError as excp:
                errorLog(excp, "Planilha 'Clientes WorkDB' não encontrada!\nNo canto inferior esquerdo, altere o nome da planilha com a lista de servidores para 'Clientes WorkDB'", writeTraceback = True, raiseError = True)
            for row in data:
                try:
                    [whitelist.append(server) for server in row.split(",")]
                except AttributeError:
                    pass
            for server,count in zip(whitelist, range(len(whitelist))):
                try:
                    print(f"Gerando Relatório {server} - {count + 1}/{len(whitelist)}")
                    id = [servidor["hostid"] for servidor in getAllServers() if servidor["host"] == server][0]
                    name = [servidor["host"] for servidor in getAllServers() if servidor["host"] == server][0]
                    self.setServers(id = id)
                    #self.serversToJSON(name = name)
                    servidorObj = self.getServer(name)
                    error = servidorObj.gerarRelatorio()
                    if not error:
                        errorLog(error = None, message = f"Modelo '{name}' não encontrado, Verifique a nomenclatura dos arquivos na pasta MODELOS")
                        errors[name] = "Modelo não encontrado, Verifique a nomenclatura dos arquivos na pasta MODELOS"
                except IndexError:
                    errorLog(None, message = f"Erro no nome '{server}' - Verifique o Nome do Servidor na planilha Excel")
                    errors[server] = f"Erro no nome - Verifique o Nome do Servidor na planilha Excel"
        else:
            id = [servidor["hostid"] for servidor in getAllServers() if servidor["host"] == nome.upper()][0]
            name = [servidor["host"] for servidor in getAllServers() if servidor["host"] == nome.upper()][0]
            self.setServers(id = id)
            #self.serversToJSON(name = name)
            servidorObj = self.getServer(name)
            error = servidorObj.gerarRelatorio()
            if not error:
                errorLog(None, message = f"Modelo '{name}' não encontrado, Verifique a nomenclatura dos arquivos na pasta MODELOS")
                errors[name] = "Modelo não encontrado, Verifique a nomenclatura dos arquivos na pasta MODELOS"
    
def printMenu():
    print("1 - Gerar todos os relatórios")
    print("2 - Gerar relatório de servidor específico")
    print("3 - Mover modelos para novo folder")
    try:
        opc = int(input())
        return opc
    except ValueError:
        print("Insira um valor númerico citado acima!")
        return None
    

if __name__ == "__main__":
    zab = Zabbix()
    while True:
        opc = printMenu()
        if opc == 1:
            system("cls")
            zab.gerarRelatorios()
            print("\n")
            for key, value in errors.items():
                print(f"Servidor '{key}' - {value}")
            input()
        elif opc == 2:
            nome = input("Insira o nome do servidor\n").upper()
            zab.gerarRelatorios(nome = nome)
        elif opc == 3:
            moverModelos()
        for key, value in errors.items():
            print(f"{key} - {value}")
        input()