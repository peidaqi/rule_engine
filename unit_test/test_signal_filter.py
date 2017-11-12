import unittest
from signal_filter import *
from signal_filter.interface import SignalStream, RuleEngine
import time

class TestSimpleRuleEngine(RuleEngine):
    def __init__(self):
        self.__rule = ""

    def load_rules(self):
        self.__rule = {"signal": "ATL2", "op": "!=", "value": "LOW", "value_type": "String"}

    def process_item(self, itm):
        if itm["signal"] == "ATL2":
            if itm["value"] == "LOW":
                return False
        return True

    def list_rules(self):
        print(self.__rule)


class TestSimpleSignalStream(SignalStream):
    def __init__(self):
        self.__count = 0

    def start_signal(self):
        print("Starting signal.")

    def next_signal(self):
        if self.__count == 0:
            return {"signal": "ATL2", "value": "LOW", "value_type": "String"}
        if self.__count == 1:
            return {"signal": "ATL2", "value": "HIGH", "value_type": "String"}
        self.__count = self.__count + 1
        return None

    def stop_signal(self):
        print("Signal stopped.")


class TestSignalFilterModule(unittest.TestCase):

    def test_signal_processor(self):
        def callback_func(itm, ret):
            if itm["value"] == "LOW":
                self.assertEqual(False, ret)
            if itm["value"] == "HIGH":
                self.assertEqual(True, ret)

        tsss = TestSimpleSignalStream()
        ts_rule_engine = TestSimpleRuleEngine()
        sp = SignalProcessor(tsss, ts_rule_engine, callback_func=callback_func)
        sp.start()
        time.sleep(5) # To make sure the SignalProcessor finishes running
        sp.stop()

    def test_json_file_rule_engine(self):
        def callback_func(itm, ret):
            if itm["value"] == "LOW":
                self.assertEqual(False, ret)
            if itm["value"] == "HIGH":
                self.assertEqual(True, ret)

        tsss = TestSimpleSignalStream()
        ts_rule_engine = JSONFileRuleEngine("unit_test\\test_rules.json")
        sp = SignalProcessor(tsss, ts_rule_engine, callback_func=callback_func)
        sp.start()
        time.sleep(5) # To make sure the SignalProcessor finishes running
        sp.stop()

    def test_json_file_signal_stream(self):
        def callback_func(itm, ret):
            if itm["value"] == "LOW":
                self.assertEqual(False, ret)
            if itm["value"] == "HIGH":
                self.assertEqual(True, ret)

        tsss = JSONFileSignalStream("unit_test\\test_raw_data.json")
        ts_rule_engine = TestSimpleRuleEngine()
        sp = SignalProcessor(tsss, ts_rule_engine, callback_func=callback_func)
        sp.start()
        time.sleep(5) # To make sure the SignalProcessor finishes running
        sp.stop()

if __name__ == "__main__":
    unittest.main()