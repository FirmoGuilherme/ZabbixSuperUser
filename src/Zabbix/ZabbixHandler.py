from src.Utils import Logger, read_from_excel
from src.Constants.Constants import CONSTANTS
from threading import Thread
from src.Zabbix.API.Server import Server

class ZabbixHandler():

	CONSTANTS = CONSTANTS
	Logger = Logger

	def __init__(self):
		self.gerar_lista_servidores()

	def gerar_lista_servidores(self):
		self.grupos_de_host = {h["name"]:h for h in
		self.CONSTANTS.ZABBIX_API.hostgroup.get(real_hosts="true",with_graphs="true") 
		if "WORKDB " not in h["name"]}
		self.hosts = {h["host"]:h for h in self.CONSTANTS.ZABBIX_API.host.get(output="extend")}

	def gerar_relatorio(self, todos = False, id = None, name = None, host_group = None):
		if todos:
			rows = read_from_excel(self.CONSTANTS.CONFIGS.excel_relatorios, "Clientes WorkDB")["Gerar Relatórios de"]
			for row in rows:
				for server in row.split(",").replace(" ", ""):
					self.gerar_relatorio(name=server)
			# abrir planilha do excel
		elif host_group:
			id = self.grupos_de_host[host_group]["groupid"]
			servidores = self.CONSTANTS.ZABBIX_API.host.get(output="extend", groupids=id)
			for raw_data in servidores:
				# START THREAD FOR EACH SERVER? MAX NUM OF THREADS?
				s = Server(raw_data)
				s.gerar_relatorio()
		elif id:
			raw_data = self.CONSTANTS.ZABBIX_API.host.get(output="extend", hostids=id)
			s = Server(raw_data[0])
			s.gerar_relatorio()

		elif name:
			id = self.hosts[name]["hostid"]
			raw_data = self.CONSTANTS.ZABBIX_API.host.get(output="extend", hostids=id)
			s = Server(raw_data[0])
			s.gerar_relatorio()



	def get_sub_menu_presentation_list(self, chosen_menu):
		if chosen_menu == "Todos":
			return [f"{len(self.grupos_de_host)} Grupos de Host"]
		elif chosen_menu == "Grupo de Hosts":
			lst = [h["name"] for h in self.grupos_de_host.values()]
			lst.sort()
			return lst
		elif chosen_menu == "Host único":
			lst = [h for h in self.hosts]
			lst.sort()
			return lst