from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject

class Item(GenericZabbixObject):

    def __init__(self, raw_data):
        super().__init__(raw_data)
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
            self.set_name()

    def set_name(self):
        ## Disk discovery
        if "vfs" in self.key_:
            self.name = self.name.replace("$1", self.key_.split("[")[1].split(",")[0])

        ## Network Interface Discovery
        elif "net" in self.key_:
            self.name = self.name.replace("$1", self.key_.split("[")[1][0:-1])

        ## Oracle Tablespace Discovery
        elif "oracle" in self.key_:
            self.name = self.name[0:-7]