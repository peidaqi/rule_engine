from signal_filter.interface import RuleEngine, SignalStream


class DummyRuleEngine(RuleEngine):
    """
    Dummy rule engine for testing the classes.
    """
    def load_rules(self):
        print("Rules loaded.")

    def process_item(self, itm):
        return "Processed" + str(itm)

    def list_rules(self):
        print("List of rules.")


class DummySignalStream(SignalStream):
    """
    Dummy signal stream for testing the classes.
    """
    def __init__(self):
        self.__count = 0

    def start_signal(self):
        print("Starting signal.")

    def next_signal(self):
        self.__count = self.__count + 1
        return self.__count

    def stop_signal(self):
        print("Signal stopped.")