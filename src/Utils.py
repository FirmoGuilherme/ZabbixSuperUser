from json import load, dump
from time import mktime
from requests import get, 
from io import BytesIO
from PIL.Image import open as readBytes
from platform import system as SYS
from urllib.parse import urlencode
from datetime import date, timedelta, datetime
from json import load
from os.path import isfile
from datetime import datetime
from traceback import format_exc



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

def loadJson(file):
    with open(file, "r") as json:
        return load(json)

def errorLog(error, message, writeTraceback = False, raiseError = False):
    mode = "a"
    if not isfile("error.log"): mode = "w"
    with open("error.log", mode) as log:
        phrase = "\n" + str(datetime.now())
        if writeTraceback:
            phrase += "\n" + format_exc()
        else:
            phrase += "\n" + message
        log.write(phrase)

    if raiseError:
        print(message)
        print("Aperte ENTER para fechar o programa!")
        input()
        raise error
    
def __readAuth():
    json_values = {}
    try:
        with open("auth.json", "r") as json:
            info = load(json)
            json_values["Url"] = info["API"]["URL"]
            json_values["User"] = info["API"]["Username"]
            json_values["Password"] = info["API"]["Password"]
        return json_values
    except FileNotFoundError as excp:
        phrase = "Arquivo de autenticação não encontrado!\n"
        phrase += """Crie um arquivo com o nome 'auth.json' e a seguinte estrutura na mesma pasta que o programa:
{
    "API": {
        "URL": "URL DO ZABBIX, ex: http://guardiao.workdb.com.br/",
        "Username": "SEU USUÁRIO",
        "Password": "SUA SENHA"
    }
}
"""
        errorLog(excp, phrase, writeTraceback = True, raiseError = True)


def remove_invalid_char(name):
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

def write_to_file(file, text):
    with open(file, "w") as txt:
        txt.write(text)

def read_from_file(file):
    with open(file, "r") as txt:
        return txt.readlines()

def write_to_json(file, data):
    with open(file, "w") as json:
        dump(data, json, indent=4)

def get_date():
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
        "tamanho",
        "size"
    ]
    allValues = []
    
    if any(x.lower() in whitelist for x in name.split()) and "percentage" not in name and "%" not in name and "Percentual" not in name:
        values = obj.histRawValues
        values.sort()
        for value in values:
            allValues.append(__convertBytes(value))
        return __convertBytes(obj.max) , __convertBytes(obj.min), __convertBytes(obj.average)

    else:
        return obj.max, obj.min, obj.average

def convertTimeFromUnix(time):
    clocks = []
    for value in time:
        clocks.append(datetime.utcfromtimestamp(int(value)))
    return clocks




def getImage(url):
    CookiesAndHeaders["Cookies"]["PHPSESSID"] = phpSessionID
    CookiesAndHeaders["Cookies"]["zbx_sessionid"] = zabbixSessionID
    response = get(url, cookies=CookiesAndHeaders["Cookies"], headers=CookiesAndHeaders["Headers"], verify=False)
    bytes = BytesIO(response.content)
    img = readBytes(bytes)
    return img




class LogsHandler():

    if not isdir("Logs"):
        mkdir("Logs")

    def __init__(self):
        self.__init_warning_Logs()
        self.__init_error_Logs()
        self.__init_info_Logs()

    def __init_error_Logs(self):
        handler = logging.FileHandler("Logs/ERROR.log")
        handler.setFormatter(logging.Formatter('\n%(asctime)s: %(message)s'))
        self.error_logger = logging.getLogger("ERROR")
        self.error_logger.setLevel(logging.ERROR)
        self.error_logger.addHandler(handler)

    def log_error(self, message, write_traceback=False):
        self.error_logger.error(message)
        if write_traceback:
            self.error_logger.error(format_exc())

    def __init_warning_Logs(self):
        handler = logging.FileHandler("Logs/WARNING.log")
        handler.setFormatter(logging.Formatter('\n%(asctime)s: %(message)s'))
        self.warning_logger = logging.getLogger("WARNING")
        self.warning_logger.setLevel(logging.WARNING)
        self.warning_logger.addHandler(handler)

    def log_warning(self, message, write_traceback=False):
        self.warning_logger.warning(message)
        if write_traceback:
            self.warning_logger.error(format_exc())

    def __init_info_Logs(self):
        handler = logging.FileHandler("Logs/INFO.log")
        handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        self.info_logger = logging.getLogger("INFO")
        self.info_logger.setLevel(logging.INFO)
        self.info_logger.addHandler(handler)

    def log_info(self, message, write_traceback=False):
        self.info_logger.info(message)
        if write_traceback:
            self.info_logger.info(format_exc())


Logger = LogsHandler()