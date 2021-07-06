from src.Configs.Configs import ConfigsHandler
from pyzabbix import ZabbixAPIException
from pyzabbix import ZabbixAPI
from requests import post

class ZabbixHandler():

	Configs = ConfigsHandler()
	
	def __init__(self):
		pass
		

	def __get_zabbix_api():
	    try:
	        API = ZabbixAPI(Configs.url)
	        API.login(user=Configs.user, password=Configs.password)
	    except ZabbixAPIException as excp:
	        errorLog(excp, "Usuário ou senha incorreta do zabbix!", writeTraceback = True, raiseError = True)
	    return API

	ZabbixAPI = __get_zabbix_api()

	def __get_sess_id(url, user, password):
	    encodedAuth = urlencode({"name": user, "password": password, "enter": ""})
	    data = post(f"{url}/index.php?{encodedAuth}")
	    zbxSessionID = data.cookies.get("zbx_sessionid")
	    phpSessionID = data.cookies.get("PHPSESSID")
	    return zbxSessionID, phpSessionID


	zabbix_session_id, php_session_id = __get_sess_id(Configs.url, Configs.user, Configs.password)

