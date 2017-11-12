from abc import ABCMeta
from abc import abstractmethod


class RuleEngine(metaclass=ABCMeta):
    """
    Abstract class for defining Rule Engines.
    Methods:
        load_rules - Load rules from an input stream.
        process_item - Process a single item. Called from SignalProceesor.run().
        list_rules - List all rules.
    """
    @abstractmethod
    def load_rules(self):
        pass

    @abstractmethod
    def process_item(self, itm):
        pass

    @abstractmethod
    def list_rules(self):
        pass


class SignalStream(metaclass=ABCMeta):
    """
    Abstract class for defining Signal Streams.
    Methods:
        start_signal - Start signal source.
        next_signal - Retrieve next signal from signal source.
        stop_signal - Stop signal source.
    """
    @abstractmethod
    def start_signal(self):
        pass

    @abstractmethod
    def next_signal(self):
        pass

    @abstractmethod
    def stop_signal(self):
        pass

