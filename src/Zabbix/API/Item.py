import time
import datetime
from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject
from .History import History

class Item(GenericZabbixObject):

    translations = {
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

    def __post_init__(self):
        if self["flags"] == "a discovered item" or "$" in self["name"]:
            self.set_name()

    def set_name(self):
        ## Disk discovery
        if "vfs" in self["key_"]:
            self["name"] = self["name"].replace("$1", self["key_"].split("[")[1].split(",")[0])

        ## Network Interface Discovery
        elif "net" in self["key_"]:
            self["name"] = self["name"].replace("$1", self["key_"].split("[")[1][0:-1])

        elif "CPU $2" in self["name"]:
            self["name"] = self["name"].replace("$2", self["key_"].split('[,')[1].strip(']'))

        ## Oracle Tablespace Discovery
        elif "oracle" in self["key_"]:
            self["name"] = self["name"][0:-7]

    def get_history(self, start_date, end_date, limit=10000) -> list:
        if type(start_date) is datetime.datetime:
            start_date = int(time.mktime(start_date.timetuple()))
        if type(end_date) is datetime.datetime:
            end_date = int(time.mktime(end_date.timetuple()))
    
        return [History(self.api, h) for h in self.api.history.get(itemids=self["itemid"], history=int(self["value_type"]), time_from=start_date, time_till=end_date,
        sortfield="clock", output="extend", sortorder="ASC", limit=limit)]
