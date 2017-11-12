from threading import Thread
from signal_filter.interface import RuleEngine, SignalStream


class SignalProcessor(Thread):
	"""
	A class to process signals using a rule engine.
	"""
	def __init__(self, ss, rule_engine, callback_func=None, sp_name=""):
		"""
		Initialize a signal processor.

		Parameters:
			ss - A SignalStream object used to provide signals.
			rule_engine - A RuleEngine object used to process signals.
			callback_func - A call back function that gets called every time after the rule_engine has processed a signal.
							Default to None.
			sp_name - A user defined identifier for the processor. Default to empty string.
		"""
		if not isinstance(ss, SignalStream):
			raise RuntimeError("First argument should be of type SignalStream.")
		self.__ss = ss
		if not isinstance(rule_engine, RuleEngine):
			raise RuntimeError("Second argument should be of type RuleEngine.")
		Thread.__init__(self)
		self.__rule_engine = rule_engine
		self.__rule_engine.load_rules()
		self.__callback_func = callback_func
		self.__output = ""
		self.__stop = False
		self.__sp_name = sp_name

	def run(self):
		"""
		Start running the processor using multi-threading. Dead-locks should be handled by user.
		"""
		self.__ss.start_signal()
		while not self.__stop:
			itm = self.__ss.next_signal()
			if itm is None:
				break
			ret = self.__rule_engine.process_item(itm)
			if self.__callback_func is not None:
				self.__callback_func(itm, ret)
		self.__ss.stop_signal()
		self.__stop = True
		pass

	def is_running(self):
		return not self.__stop

	def stop(self):
		"""
		Stop the processor.
		"""
		self.__stop = True
