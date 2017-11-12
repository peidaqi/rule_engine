from signal_filter import *
import sys

if not sys.version[0] == "3":
	raise RuntimeError("This program requires Python 3.x!")

def ml_call_back(itm, ret):
	if ret is False:
		print("Signal ", itm["signal"], " filtered out.")
		return
	#
	# Here we can do some further processing of the non-filtered signal data, e.g. call some machine learning routines
	#
	return

fss1 = JSONFileSignalStream("raw_data.json")

rule_engine = JSONFileRuleEngine("rules.json")
rule_engine.load_rules()
sp1 = SignalProcessor(fss1, rule_engine, sp_name="Processor 1", callback_func=ml_call_back)

sp1.start()
while sp1.is_running():
	pass
# sp1.stop()  # We can stop the SignalProcessor before all signals processed.
