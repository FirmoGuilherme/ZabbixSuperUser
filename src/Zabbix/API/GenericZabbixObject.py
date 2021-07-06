from abc import ABC, ABCMeta, abstractmethod



class GenericZabbixObject(ABC):
    '''
    @abstractmethod = função obrigatória de ser implementada em cada tipo de TestCase
    '''
    __metaclass__ = ABCMeta

	def __init__(self, raw_data):
		for attribute, value in raw_data.items():
			if all([char in "1234567890" for char in value]):
				translation = self.__translate(attribute, value)

	@abstractmethod
	def __translate(self, attribute, value):
		pass