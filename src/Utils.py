from os import path, mkdir
import logging
from json import dump, load
from traceback import format_exc

def remove_invalid_char(name):
    blacklist = [
        "{$SID}", 
        "(SEG)",
        "$1",
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
    for char in blacklist:
        filtered = filtered.replace(char, "")

    while len(filtered) > 0:
        if filtered[-1] == " ":
            filtered = filtered[0:-1]
            continue
        break
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

def read_from_json(file):
    return load(open(file, "r"))

def read_from_excel(file, sheet_name = None):
    if sheet_name:
        return pd.read_excel(file, sheet_name=sheet_name)
    else:
        return pd.read_excel(file)

class LogsHandler():

    if not path.isdir("Logs"):
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