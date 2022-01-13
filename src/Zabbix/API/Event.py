from src.Zabbix.API.GenericZabbixObject import GenericZabbixObject

class Event(GenericZabbixObject):

    translations = {
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