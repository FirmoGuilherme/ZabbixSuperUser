from json import load
from datetime import datetime
from pyzabbix import ZabbixAPI
from time import time
from requests import get, post
from io import BytesIO
from PIL.Image import open as readBytes
from platform import system as SYS


class errorHandler(Exception):

    def __init__(self, error):
        with open("error.log", "a") as log:
            log.write(f"\n{datetime.now()} -     ")
            log.write(error)
        if error == "auth.json not found":
            phrase = f"\n{datetime.now()}"
            phrase += "\nArquivo auth.json não encontrado!"
        super().__init__(phrase)
        
def __readAuth():
    json_values = {}
    try:
        with open("auth.json", "r") as json:
            info = load(json)
            json_values["Url"] = info["Website"]["Url"]
            json_values["Cookies"] = info["Website"]["Cookies"]
            json_values["Headers"] = info["Website"]["Headers"]
            json_values["User"] = info["API"]["Username"]
            json_values["Password"] = info["API"]["Password"]
        return json_values
    except FileNotFoundError:
        raise errorHandler(error = "auth.json not found")

def getZabbixAPI():
    Auth = __readAuth()
    API = ZabbixAPI(Auth["Url"])
    API.login(Auth["User"], Auth["Password"])
    
    return API



def getImage(url, zbxsessID, phpsessID):
    Auth = __readAuth()
    print(f"zbxsessID = {zbxsessID}")
    print(f"phpsessID = {phpsessID}")
    Auth["Cookies"]["PHPSESSID"] = phpsessID
    Auth["Cookies"]["zbx_sessionid"] = zbxsessID
    print(Auth["Cookies"])
    response = get(url, cookies=Auth["Cookies"], headers=Auth["Headers"], verify=False)
    bytes = BytesIO(response.content)
    img = readBytes(bytes)
    return img

def getSessID():
    payload = {"name": "lucas.hoeltgebaum", "passsword": "2021#Workdb"}
    zbxSessionID = post("http://guardiao.workdb.com.br/zabbix.php", data=payload).cookies.get("zbx_sessionid")
    phpSessionID = get("http://guardiao.workdb.com.br/index.php?action=dashboard.view", data=payload).cookies.get("PHPSESSID") 
    return zbxSessionID, phpSessionID

def getOS():
    sys = SYS()
    if sys.lower() == "linux": return "linux"
    elif sys.lower() == "windows": return "windows"
        
def getBar():
    sys = getOS()
    if sys == "linux": return "/"
    elif sys == "windows": return "\\"
        
def removeInvalidChar(name):
    words_blacklist = [
    "{$SID}", 
    "(SEG)",
    "$1"
    ]
    char_blacklist = [
        "\\",
        "/",
        ":",
        "?",
        '"'
        "<",
        ">",
        "|"
    ]
    filtered = name
    for word in words_blacklist:
        if word in name:
            filtered = name.replace(word, "")
    for char in char_blacklist:
        if char in name:
            filtered = filtered.replace(char, "")
    return filtered

def getTime(function):
    print("STAR TIME")
    start = time()
    function()
    end = time()
    print(end - start)








if __name__ == "__main__":
    zbx, php = getSessID()
    img = getImage("http://guardiao.workdb.com.br/chart2.php?graphid=19561&from=now-1h&to=now&profileIdx=web.graphs.filter&profileIdx2=19561&width=1567&height=201&_=uq4xhrg6",zbx, php)
    img.show()