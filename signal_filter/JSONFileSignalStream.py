from signal_filter.interface import SignalStream
import json


class JSONFileSignalStream(SignalStream):
	"""
	A class for loading signals from a JSON file. Current implementation caches the entire file.
	"""
	def __init__(self, filename):
		self.__count = 0
		self.__filename = filename
		self.__file = None
		self.__json_buf = None

	def start_signal(self):
		"""
		Load signal from JSON file.
		"""
		self.__file = open(self.__filename, "r")
		self.__json_buf = json.JSONDecoder().decode(self.__file.read())

	def next_signal(self):
		"""
		Get next signal from the cached JSON file.
		"""
		ret = None
		if self.__count < len(self.__json_buf):
			ret = self.__json_buf[self.__count]
		self.__count = self.__count + 1
		return ret

	def stop_signal(self):
		"""
		Destroy the cached JSON file and close file handle.
		"""
		del self.__json_buf # GC the cached file.
		self.__file.close()
