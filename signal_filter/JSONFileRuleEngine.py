from signal_filter.interface import RuleEngine
from dateutil import parser
import json
import datetime


class JSONFileRuleEngine(RuleEngine):
	"""
	A class for loading rules from a JSON file.
	"""
	def __init__(self, filename):
		self.__rules = {}
		self.__filename = filename

	def load_rules(self):
		"""
		Load rules from file. Note here the entire rules file is loaded, so it may take some time to load large files.
		"""
		f = open(self.__filename, "r")
		content = f.read()
		rule_list = json.JSONDecoder().decode(content)

		for rule in rule_list:
			op_list = self.__rules.get(rule["signal"].strip(), [])
			op_list.append({"op": rule["op"].strip(), "value": rule["value"].strip(), "value_type": rule["value_type"].strip()})
			self.__rules[rule["signal"]] = op_list
		f.close()

	def process_item(self, itm):
		"""
		Process a single item from the signal source.

		Parameters:
			itm - the item from the signal source.

		Returns:
			Whether the item passes the rules test (True/False).
		"""
		ret = True  # if there're no rules to apply
		rules = self.__rules.get(itm["signal"], None)
		if rules is None:
			return ret
		for rule in rules:
			if itm["value_type"].lower() != rule["value_type"].lower():
				break
			value = None
			value_to_compare = None
			try:
				if itm["value_type"].lower() == "integer":  # In case we have a mix of lower/upper cases.
					value = float(rule["value"])  # The raw data provided seems to be float rather than int.
					value_to_compare = float(itm["value"])
				if itm["value_type"].lower() == "datetime":
					if rule["value"] == "TODAY":  # Added a custom function "TODAY" for getting today's date.
						value = datetime.datetime.today()
					else:
						value = parser.parse(rule["value"])
					value_to_compare = parser.parse(itm["value"])
				if itm["value_type"].lower() == "string":
					value = rule["value"].strip()
					value_to_compare = itm["value"].strip()

				if rule["op"] == ">":
					ret = (value_to_compare > value) and ret
				if rule["op"] == "==":
					ret = (value_to_compare == value) and ret
				if rule["op"] == "<":
					ret = (value_to_compare < value) and ret
				if rule["op"] == "!=":
					ret = (value_to_compare != value) and ret
			except Exception as e:
				print("*************** Runtime Error Dump ***************")
				print("Item is: ", itm)
				print("Rule is: ", rule)
				raise e
		return ret

	def list_rules(self):
		"""
		Print out all rules to stdout.
		"""
		for k in self.__rules.keys():
			print("Rules for signal ", k)
			for op_val in self.__rules[k]:
				print("Op: ", op_val["op"], " Value: ", op_val["value"], " Value type: ", op_val["value_type"])
