from json import load
from datetime import datetime
from pyzabbix import ZabbixAPI


class errorHandler(Exception):

    def __init__(self, error):
        with open("error.log", "a") as log:
            log.write(f"\n{datetime.now()}")
            log.write(error)
        if error == "auth.json not found":
            phrase = f"\n{datetime.now()}"
            phrase += "\nArquivo auth.json não encontrado!"
        super().__init__(phrase)

def readAuth():
    json_values = {}
    try:
        with open("auth.json", "r") as json:
            info = load(json)
            json_values["url"] = info["Website"]["url"]
            json_values["cookies"] = info["Website"]["cookies"]
            json_values["headers"] = info["Website"]["headers"]
            json_values["user"] = info["API"]["Username"]
            json_values["password"] = info["API"]["Password"]
        return json_values
    except FileNotFoundError:
        raise errorHandler(error = "auth.json not found")

def getZabbixAPI():
    Auth = readAuth()
    API = ZabbixAPI(Auth["url"])
    API.login(Auth["user"], Auth["password"])
    
    return API


def removeInvalidChar(name):
    words_blacklist = [
    "{$SID}", 
    "(SEG)",
    "$1"
    ]
    char_blacklist = [
        "/",
        "º",
        "-",
        "#"
    ]
    filtered = name
    for word in words_blacklist:
        if word in name:
            filtered = name.replace(word, "")
    for char in char_blacklist:
        if char in name:
            filtered = filtered.replace(char, "")
    return filtered