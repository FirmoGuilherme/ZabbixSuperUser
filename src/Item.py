from time import mktime
from datetime import datetime
from src.Utils import ZabbixAPI, translateBytes

time_end = int(mktime(datetime.now().timetuple()))
time_start = time_end - 60 * 60 * 24 * 31

class Item():

    def __init__(self, raw_data):
        blacklist = [
            "itemid",
            "hostid",
            "trends",
            "history",
            "templateid",
            "valuemapid",
            "interfaceid",
            "inventory_link",
            "evaltype",
            "master_itemid",
            "query_fields",
            "status_codes",
            "headers",
            "lastclock",
            "lastns",
            "lifetime",
            "lastvalue",
            "prevvalue",
            "delay"
            ]
        for attribute in raw_data.keys():
            setattr(self, attribute, raw_data[attribute])
            try:
                if raw_data[attribute].isnumeric():
                    self.__translateNumeric(attribute, raw_data[attribute])
            except AttributeError: pass
        """
            itemid
            type
            snmp_community
            snmp_oid
            hostid
            name
            key_
            delay
            history
            trends
            status
            value_type
            trapper_hosts
            units
            snmpv3_securityname
            snmpv3_securitylevel
            snmpv3_authpassphrase
            snmpv3_privpassphrase
            formula
            logtimefmt
            templateid
            valuemapid
            params
            ipmi_sensor
            authtype
            username
            password
            publickey
            privatekey
            flags
            interfaceid
            port
            description
            inventory_link
            lifetime
            snmpv3_authprotocol
            snmpv3_privprotocol
            snmpv3_contextname
            evaltype
            jmx_endpoint
            master_itemid
            timeout
            url
            query_fields
            posts
            status_codes
            follow_redirects
            post_type
            http_proxy
            headers
            retrieve_mode
            request_method
            output_format
            ssl_cert_file
            ssl_key_file
            ssl_key_password
            verify_peer
            verify_host
            allow_traps
            state
            error
            lastclock
            lastns
            lastvalue
            prevvalue
        """
        if self.flags == "a discovered item":
            self.setName()

    def setName(self):
        ## Disk discovery
        if "vfs" in self.key_:
            self.name = self.name.replace("$1", self.key_.split("[")[1].split(",")[0])

        ## Network Interface Discovery
        elif "net" in self.key_:
            self.name = self.name.replace("$1", self.key_.split("[")[1][0:-1])

        ## Oracle Tablespace Discovery
        elif "oracle" in self.key_:
            self.name = self.name[0:-7]
        

    def __translateNumeric(self , attribute, value):
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
        try: setattr(self, attribute, translations[attribute][int(value)])
        except KeyError: pass

    def getHistory(self):
        self.rawHistory = ZabbixAPI.history.get(itemids = self.itemid, time_from=time_start, time_till=time_end, output='extend', limit='10000000')
        self.histRawValues = [float(hist["value"]) for hist in self.rawHistory]
        self.max = max(self.histRawValues)
        self.min = min(self.histRawValues)
        self.average = sum(self.histRawValues) / len(self.histRawValues)

    def convertHistory(self):
        self.max, self.min, self.average = translateBytes(self, self.name)
