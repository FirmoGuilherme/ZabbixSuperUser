from src.Configs.Configs import ConfigsHandler
from src.Utils import Logger
from requests import post
from urllib.parse import urlencode
from pyzabbix import ZabbixAPIException, ZabbixAPI

class CONSTANTS():

	CONFIGS = ConfigsHandler()

	COOKIES = {
	"PHPSESSID": "",
	"zbx_sessionid": ""
	}

	HEADERS = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
		"Content-Type": "application/x-www-form-urlencoded",
		"Origin": CONFIGS.url[0:-1],
		"Connection": "keep-alive",
		"Referer": f"{CONFIGS.url}index.php",
		"Upgrade-Insecure-Requests": "1"
	}

	EVENT = {
		"source":{
			0: "event created by a trigger",
			1: "event created by a discovery rule",
			2: "event created by active agent auto-registration",
			3: "internal event",
		},
		"object":{
			0: "trigger",
			1: "discovered host",
			2: "discovered service",
			3: "auto-registered host",
			4: "item",
			5: "LLD rule"
		},
		"value":{
			0: "OK",
			1: "problem / host or service down / unknown or not supported state",
			2: "host or service discovered",
			3: "host or service lost"
		},
		"severity":{
			0: "not classified",
			1: "information",
			2: "warning",
			3: "average",
			4: "high",
			5: "disaster"
		},
		"suppressed":{
			0: "event is in normal state",
			1: "event is supressed"
		},
		"acknowledged": {
			0: "No",
			1: "Yes"
		}
	}

	GRAPH = {            
		"flags":{
			0: "(default) a plain graph",
			4: "a discovered graph"
		},
		"graphtype":{
			0: "(default) normal)",
			1: "stacked",
			2: "pie",
			3: "exploded",
		},
		"show_3d":{
			0: "(default) show in 2D",
			1: "show in 3d",
		},
		"show_legend":{
			0: "hide",
			1: "(default) show"
		},
		"show_work_period":{
			0: "hide",
			1: "(default) show",
			2: "NTLM"
		},
		"show_triggers":{
			0: "hide",
			1: "(default) show"
		},
		"ymax_type":{
			0: "(default) calculated",
			1: "fixed",
			2: "item"
		},
		"ymin_type":{
			0: "(default) calculated",
			1: "fixed",
			2: "item"
			}
		}

	ITEM = {
		"type":{
			0: "Zabbix agent",
			1: "SNMPv1 agent",
			2: "Zabbix trapper",
			3: "simple check",
			4: "SNMPv2 agent",
			5: "Zabbix internal",
			6: "SNMPv3 agent",
			7: "Zabbix agent (active)",
			8: "Zabbix aggregate",
			9: "web item",
			10: "external check",
			11: "database monitor",
			12: "IPMI agent",
			13: "SSH agent",
			14: "TELNET agent",
			15: "calculated",
			16: "JMX agent",
			17: "SNMP trap",
			18: "Dependent item",
			19: "HTTP agent", 
		},
		"value_type":{
			0: "numeric float",
			1: "character",
			2: "log",
			3: "numeric unsigned",
			4: "text"
		},
		"allow_traps":{
			0: "(default) Do not allow to accept incoming data",
			1: "Allow to accept incoming data"
		},
		"authtype":{
			0: "(default) none",
			1: "basic",
			2: "NTLM"
		},
		"flags":{
			0: "a plain item",
			4: "a discovered item"
		},
		"follow_redirects":{
			0: "Do not follow redirects",
			1: "(default) Follow redirects"
		},
		"output_format":{
			0: "(default) Store raw",
			1: "Convert to JSON"
		},
		"post_type":{
			0: "(default) Raw data",
			2: "JSON data",
			3: "XML data"
		},
		"request_method":{
			0: "(default) set",
			1: "POST",
			2: "PUT",
			3: "HEAD"
		},
		"retrieve_mode":{
			0: "(default) Body",
			1: "Headers",
			2: "Both body and headers will be stored"
		},
		"snmpv3_authprotocol":{
			0: "(default) MD5",
			1: "SHA"
		},
		"snmpv3_privprotocol":{
			0: "(default) DES",
			1: "AES"
		},
		"snmpv3_securitylevel":{
			0: "noAuthNoPriv",
			1: "atuHnoPriv",
			2: "authPriv"
		},
		"state":{
			0: "(default) normal",
			1: "not supported"
		},
		"status":{
			0: "(default) enabled item",
			1: "disabled item"
		},
		"verify_host":{
			0: "(default) Do not validate",
			1: "Validate"
		},
		"verify_peer":{
			0: "(default) Do not validate",
			1: "Validate"
			}
	}

	SERVER = {
		"available":{
			0: "(default) unknow",
			1: "available",
			2: "unavailable"
		},
		"flags":{
			0: "a plain host",
			4: "a discovered host"
		},
		"inventory_mode":{
		   -1: "disabled",
			0: "(default) normal",
			1: "automatic"
		},
		"ipmi_authtype":{
		   -1: "(default) default",
			0: "none",
			1: "MD2",
			2: "MD5",
			4: "straight",
			5: "OEM",
			6: "RMCP+"
		},
		"ipmi_available":{
			0: "(default) unknow",
			1: "available",
			2: "unavailable"
		},
		"ipmi_privilege":{
			1: "callback",
			2: "(default) user",
			3: "operator",
			4: "admin",
			5: "OEM"
		},
		"jxm_available":{
			0: "(default) unknow",
			1: "available",
			2: "unavailable"
		},
		"maintenance_status":{
			0: "(default) no maintenance",
			1: "maintenance in effect"
		},
		"maintenance_type":{
			0: "(default) maintenance with data collection",
			1: "maintenance without data collection"
		},
		"snmp_available":{
			0: "(default) unkown",
			1: "available",
			2: "unavailable"
		},
		"status":{
			0: "(default) No encryption",
			1: "unmonitored host"
		},
		"tls_connect":{
			0: "(default) No encryption",
			1: "PSK",
			4: "certificate"
		},
		"tls_accept":{
			1: "(default) No encryption",
			2: "PSK",
			4: "certificate"
		}
	}

	def __set_session_id(url, user, password):
		encodedAuth = urlencode({"name": user,"password": password, "enter": ""})
		data = post(f"{url}/index.php?{encodedAuth}")
		zbxSessionID = data.cookies.get("zbx_sessionid")
		phpSessionID = data.cookies.get("PHPSESSID")
		return zbxSessionID, phpSessionID

	ZABBIX_SESSION_ID, PHP_SESSION_ID = __set_session_id(CONFIGS.url, CONFIGS.user, CONFIGS.password)
	COOKIES["PHPSESSID"] = PHP_SESSION_ID
	COOKIES["zbx_sessionid"] = ZABBIX_SESSION_ID

	def __get_zabbix_api(url, user, password):
	    try:
	        API = ZabbixAPI(url)
	        API.login(user=user, password=password)
	    except ZabbixAPIException as excp:
	        Logger.log_error(message = "Usuário ou senha incorreta do zabbix!", write_traceback = True)
	  		# Way to inform user that error occurred?
	    return API

	ZABBIX_API = __get_zabbix_api(CONFIGS.url, CONFIGS.user, CONFIGS.password)