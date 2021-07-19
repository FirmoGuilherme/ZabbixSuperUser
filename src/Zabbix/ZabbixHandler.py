from src.Utils import Logger, read_from_excel, Thread
from src.Constants.Constants import CONSTANTS
from src.Zabbix.API.Server import Server
from time import sleep
from tkinter import messagebox



class ZabbixHandler():

	CONSTANTS = CONSTANTS
	Logger = Logger

	def __init__(self):
		#self.input_from = input_from
		#self.input_to = input_to
		pass

	def gerar_lista_servidores(self):
		try:	
			self.grupos_de_host = {h["name"]:h for h in
			self.CONSTANTS.ZABBIX_API.hostgroup.get(real_hosts="true",with_graphs="true") 
			if "WORKDB " not in h["name"]}
		except AttributeError:
			return AttributeError
		self.hosts = {h["host"]:h for h in self.CONSTANTS.ZABBIX_API.host.get(output="extend")}
		return True

	def gerar_relatorio(self, 
		start_date, 
		end_date,
		todos = False, host_group = None,
		id = None, name = None, 
		return_th = False):
		while True:
			if Thread.get_amount_running_threads() > 5:
				sleep(2)
				continue
			zab_start_date = f"{start_date.year}-{start_date.month}-{start_date.day} 00:00:00"
			zab_end_date = f"{end_date.year}-{end_date.month}-{end_date.day} 23:59:59"
			errors = []
			threads = []
			if todos:
				rows = read_from_excel(self.CONSTANTS.CONFIGS.excel_relatorios, "Clientes WorkDB")["Gerar Relatórios de"]
				for row in rows:
					for server in [s.replace(" ", "") for s in row.split(",")]:
						th = self.gerar_relatorio(name=server, return_th = True, 
							start_date=start_date, end_date=end_date)
						threads.append(th)
			elif host_group:
				id = self.grupos_de_host[host_group]["groupid"]
				servidores = self.CONSTANTS.ZABBIX_API.host.get(output="extend", groupids=id)
				for raw_data in servidores:
					# START THREAD FOR EACH SERVER? MAX NUM OF THREADS?
					th = self.gerar_relatorio(name=raw_data["host"], return_th = True, 
						start_date=start_date, end_date=end_date)
					threads.append(th)
			elif id:
				raw_data = self.CONSTANTS.ZABBIX_API.host.get(output="extend", hostids=id)
				th = Thread(target = Server(raw_data[0]).gerar_relatorio, 
					start_date=zab_start_date, end_date=zab_end_date).start()
				threads.append(th)
				if return_th:
					return th

			elif name:
				id = self.hosts[name]["hostid"]
				raw_data = self.CONSTANTS.ZABBIX_API.host.get(output="extend", hostids=id)
				th = Thread(target = Server(raw_data[0]).gerar_relatorio, 
					start_date=zab_start_date, end_date=zab_end_date).start()
				threads.append(th)
				if return_th:
					return th
			for th in threads:
				error, name = th.result()
				if error == FileNotFoundError:
					errors.append("Modelo {} não encontrado!".format(name))
			print(errors)
			return errors

	def get_sub_menu_presentation_list(self, chosen_menu):
		if chosen_menu == "Todos":
			return ["Planilha Excel"]
		elif chosen_menu == "Grupo de Hosts":
			lst = [h["name"] for h in self.grupos_de_host.values()]
			lst.sort()
			return lst
		elif chosen_menu == "Host único":
			lst = [h for h in self.hosts]
			lst.sort()
			return lst