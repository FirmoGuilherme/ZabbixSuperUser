from os import path, mkdir
import logging
import datetime
from dateutil import parser
from json import dump, load
from traceback import format_exc
import concurrent.futures
import pandas as pd
import time

class Thread():

    all_threads = []
    ThreadPoolExecutor = concurrent.futures.ThreadPoolExecutor()

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def get_amount_running_threads():
        return Thread.ThreadPoolExecutor._work_queue.qsize()

    def start(self):
        try:
            if self.args:
                new = Thread.ThreadPoolExecutor.submit(
                    lambda: self.target(*self.args))
            elif self.kwargs:
                new = Thread.ThreadPoolExecutor.submit(
                    lambda: self.target(**self.kwargs))
            else:
                new = Thread.ThreadPoolExecutor.submit(self.target)
        except:
            pass
        Thread.all_threads.append(new)
        return new

    def exit():
        for count, th in enumerate(Thread.all_threads):
            if th.exception():
                try:
                    th.result()
                except Exception as excp:
                    Logger.log_error(f"{excp}\n")
            try:
                th.set_result("finished")
            except:
                continue

def hex_to_rgb(hex):
  rgb = []

  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal / 1000)

  return tuple(rgb)

def days_difference(start, end):
    duration = end - start
    duration_in_s = duration.total_seconds()  
    days  = duration.days 
    days  = divmod(duration_in_s, 86400)[0]
    return days + 1

def get_time_difference(time1, time2):
    time1 = format_datetime(time1)
    time2 = format_datetime(time2)
    return abs(time.mktime(time1.timetuple()) - time.mktime(time2.timetuple()))


def format_datetime(arg_date):
    if arg_date is not None:
        if type(arg_date) is not datetime.datetime:
            try:
                if 'Z' in arg_date or str(arg_date).count(':') == 3:
                    arg_date = parser.parse(arg_date)
                elif str(arg_date).count("/") == 2 and str(arg_date).count(":") == 2:
                    if "PM" not in arg_date and "AM" not in arg_date:
                        day, month = arg_date.split("/")[0:2]
                        arg_date = arg_date.replace(
                            f"{day}/{month}", r"{day}/{month}")
                        arg_date = arg_date.format(day=month, month=day)
                    arg_date = parser.parse(arg_date+"-03:00")
                else:
                    arg_date = parser.parse(arg_date+"-03:00")
            except Exception:
                arg_date = parser.parse(arg_date)
    return arg_date

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