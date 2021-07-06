from src.Configs.Configs import ConfigsHandler
from src.Constants.Constants import CONSTANTS
from src.Utils import remove_invalid_char


class GenericZabbixObject():
	
	CONSTANTS = CONSTANTS

	def __init__(self, raw_data):
		for attribute, value in raw_data.items():
			if value != "" and type(value) in (str, int, float):
				if all([char in "1234567890" for char in value]):
					translation = self.__translate_numbers(attribute, value)
					setattr(self, remove_invalid_char(attribute), translation)
				else:
					if attribute != "host":
						setattr(self, remove_invalid_char(attribute), remove_invalid_char(value))
					else:
						setattr(self, remove_invalid_char(attribute), value)
			elif value == "":
				setattr(self, remove_invalid_char(attribute), None)

			elif type(value) == list:
				setattr(self, attribute, value)

	def __translate_numbers(self, attribute, value):
		translations = CONSTANTS.__dict__.get(self.__class__.__name__.upper())
		if attribute in translations.keys():
			if int(value) in translations.get(attribute):
				return translations.get(attribute).get(int(value))
			else:
				return int(value)
		else:
			return int(value)