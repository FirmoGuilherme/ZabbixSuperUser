from json import dump, load
from os.path import isfile, join
from os import makedirs
from copy import copy
from base64 import b64encode, b64decode
from src.Utils import Logger, write_to_json, read_from_json
from traceback import format_exc
from json.decoder import JSONDecodeError

path = []
result = []



class ConfigsHandler():

    def __init__(self):
        self.__set_all_attributes(parentAttr=self.__get_configs())
        self.__create_storage_folders()
        self.__decode_password()

    def __set_all_attributes(self, parentAttr):
        for key, value in parentAttr.items():
            if type(value) != dict:
                if "/" in str(value) and "http" not in value:
                    value = join(*[folder for folder in value.split("/")])
                elif "\\" in str(value) and "http" not in value:
                    value = join(*[folder for folder in value.split("\\")])
                setattr(self, key, value)
            elif type(value) == dict:
                self.__set_all_attributes(value)

    def __create_storage_folders(self):
        folders_list = [value for key, value in self.__dict__.items() if "storage" in key]
        for folder_path in folders_list:
            try:
                makedirs(folder_path)
            except FileExistsError:
                pass

    def __decode_password(self):
        self.password = str(b64decode(self.password))[2:-1]

    def __get_configs(self):
        defaults = {
            "Web": {
                "url": "http://guardiao.workdb.com.br/"
            },
            "Directories": {
                "modelos_storage": "Modelos",
                "relatorios_storage": "Relatorios",
                "excel_relatorios": "Relação Clientes Monitoramento Relatório.xlsx"
            },
            "Credentials": {
                "user": "lucas.hoeltgebaum",
                "password": ""
            }
        }

        if isfile(".configs.json"):
            try:
                return read_from_json(".configs.json")
            except JSONDecodeError:
                return defaults
        else:
            Logger.log_warning(
                message=".configs.json não encontrado, usando valores Default", write_traceback=False)
            return defaults

    def save_configs(self, new_config):
        current_config = self.__get_configs()
        for key, value in new_config.items():
            self.__iter_configs(key=key)
            path_to_config = result[0]
            if key == "password":
                value = str(b64encode(value.encode("utf-8")))[2:-1]
            current_config[path_to_config[0]][key] = value
        write_to_json(".configs.json", current_config)

    def __iter_configs(self, dict_obj=None, key=None, i=None):
        if not dict_obj:
            path.clear()
            result.clear()
            dict_obj = self.__get_configs()
        for k, v in dict_obj.items():
            # add key to path
            path.append(k)
            if isinstance(v, dict):
                # continue searching
                self.__iter_configs(v, key, i)
            if isinstance(v, list):
                # search through list of dictionaries
                for i, item in enumerate(v):
                    # add the index of list that item dict is part of, to path
                    path.append(i)
                    if isinstance(item, dict):
                        # continue searching in item dict
                        self.__iter_configs(item, key, i)
                    # if reached here, the last added index was incorrect, so removed
                    path.pop()
            if k == key:
                # add path to our result
                result.append(copy(path))
            # remove the key added in the first line
            if path != []:
                path.pop()

    def translate(self, key, reverse=False):
        translations = {"url": "URL", "modelos_storage": "Folder com Modelos",
                        "relatorios_storage": "Folder para criar Relatorios", "user": "Usuário no Zabbix",
                        "password": "Senha no Zabbix", "excel_relatorios": "Servidores p/ gerar Relatorios"}
        if not reverse:
            return translations.get(key, key.capitalize())
        else:
            try:
                idx = list(translations.values()).index(key)
                return list(translations.keys())[idx]
            except ValueError:
                return key.lower()
