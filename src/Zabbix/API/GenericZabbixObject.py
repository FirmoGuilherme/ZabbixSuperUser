from src.Configs.Configs import ConfigsHandler
from src.Constants.Constants import CONSTANTS
from src.Utils import remove_invalid_char


class GenericZabbixObject(dict):

	translations = {}

	def __init__(self, api, raw_data):
		super().__init__()
		self.api = api
		self.raw_data = raw_data
		for attribute, value in raw_data.items():
			if value and type(value) in (str, int, float):
				if all(char in "1234567890" for char in str(value)):
					translation = self._translate_numbers(attribute, value)
					self[remove_invalid_char(attribute)] = translation
				elif attribute != "host":
					self[remove_invalid_char(attribute)] = remove_invalid_char(value)
				else:
					self[remove_invalid_char(attribute)] = value
			elif not value:
				self[remove_invalid_char(attribute)] = None

			elif type(value) is list:
				self[attribute] = value
				
		self.__post_init__()

	def _translate_numbers(self, attribute, value):
		if not self.translations or not self.translations.get(attribute):
			return int(value)
		if int(value) in self.translations.get(attribute):
			return self.translations.get(attribute).get(int(value))
		else:
			return int(value)

	def __setitem__(self, key, value):
		super().__setitem__(key, value)

	def __getitem__(self, key):
		return super().__getitem__(key)

	def __post_init__(self):
		return