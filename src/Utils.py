from json import load, dump
from pyzabbix import ZabbixAPI
from time import mktime
from requests import get, post
from io import BytesIO
from PIL.Image import open as readBytes
from platform import system as SYS
from urllib.parse import urlencode
from datetime import date, timedelta, datetime
from json import load




CookiesAndHeaders = {
        "Cookies": {
            "PHPSESSID": "",
            "zbx_sessionid": ""
        },
        "Headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://guardiao.workdb.com.br",
            "Connection": "keep-alive",
            "Referer": "http://guardiao.workdb.com.br/index.php",
            "Upgrade-Insecure-Requests": "1"
        }
    }


class errorHandler(Exception):

    def __init__(self, error):
        with open("error.log", "a") as log:
            log.write(f"\n{datetime.now()} -     ")
            log.write(error)
        if error == "auth.json not found":
            phrase = f"\n{datetime.now()}"
            phrase += "\nArquivo auth.json não encontrado!"
        super().__init__(phrase)

def loadJson(file):
    with open(file, "r") as json:
        return load(json)


def __readAuth():
    """
        {
            "API": {
                "URL": "",
                "Username": "",
                "Password": ""
            }
        }
    """
    json_values = {}
    try:
        with open("auth.json", "r") as json:
            info = load(json)
            json_values["Url"] = info["API"]["URL"]
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
    CookiesAndHeaders["Cookies"]["PHPSESSID"] = phpsessID
    CookiesAndHeaders["Cookies"]["zbx_sessionid"] = zbxsessID
    response = get(url, cookies=CookiesAndHeaders["Cookies"], headers=CookiesAndHeaders["Headers"], verify=False)
    bytes = BytesIO(response.content)
    img = readBytes(bytes)
    return img

def getSessID():
    Auth = __readAuth()
    encodedAuth = urlencode({"name": Auth["User"], "password": Auth["Password"], "enter": ""})
    data = post("http://guardiao.workdb.com.br/index.php?{}".format(encodedAuth))
    zbxSessionID = data.cookies.get("zbx_sessionid")
    phpSessionID = data.cookies.get("PHPSESSID")
    return zbxSessionID, phpSessionID

def getOS():
    sys = SYS()
    if sys.lower() == "linux": return "linux"
    elif sys.lower() == "windows": return "windows"
        
def toJSON(attributes, values, file):
    config = {}
    for attribute, value in zip(attributes, values):
        if type(value) == str or type(value) == int and len(str(value)) >= 1:
            config[attribute] = value
    with open(file, "w") as json:
        dump(config, json, indent = 4)

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
        '"',
        "<",
        ">",
        "|",
        "%",
        "*",
        "-"
    ]
    filtered = name
    for word in words_blacklist:
        if word in name:
            filtered = name.replace(word, "")
    for char in char_blacklist:
        if char in name:
            filtered = filtered.replace(char, "")
    while filtered[-1] == " ":
        filtered = filtered[0:-1]
    return filtered

def getDate():
    lastDay = (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y%m%d")
    firstDay = lastDay[0:-2] + "01"
    lastDay = datetime(int(lastDay[0:4]), int(lastDay[4:6]), int(lastDay[6:]), 23 ,59 ,59)
    firstDay = datetime(int(firstDay[0:4]), int(firstDay[4:6]), int(firstDay[6:]))
    lastDay = int(mktime(lastDay.timetuple()))
    firstDay = int(mktime(firstDay.timetuple()))
    return firstDay, lastDay

def __convertBytes(Bytes):
    Bytes = float(Bytes)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if Bytes < KB:
        return '{0} {1}'.format(Bytes,'Bytes' if 0 == Bytes > 1 else 'Byte')
    elif KB <= Bytes < MB:
        return '{0:.2f} KB'.format(Bytes/KB)
    elif MB <= Bytes < GB:
        return '{0:.2f} MB'.format(Bytes/MB)
    elif GB <= Bytes < TB:
        return '{0:.2f} GB'.format(Bytes/GB)
    elif TB <= Bytes:
        return '{0:.2f} TB'.format(Bytes/TB)

def translateBytes(obj, name):
    whitelist = [
        "disk",
        "memory",
        "swap",
        "tamanho"
    ]
    allValues = []
    
    if any(x.lower() in whitelist for x in name.split()) and "percentage" not in name and "%" not in name and "Percentual" not in name:
        values = [data["value"] for data in obj.history]
        values.sort()
        for value in values:
            allValues.append(__convertBytes(value))
        return allValues, __convertBytes(obj.max), __convertBytes(obj.min) , __convertBytes(obj.average)
    else:
        return obj.allValues, obj.max, obj.min, obj.average

def convertTimeFromUnix(time):
    clocks = []
    for value in time:
        clocks.append(datetime.utcfromtimestamp(int(value)))
    return clocks