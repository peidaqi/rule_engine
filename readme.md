## Rule based Signal Processing

by Daqi Pei Nov. 2017



**Introduction**

​	The task is to build a tool for processing signals based on a preset set of rules. The input file is given as a JSON format, and naturally Python is chosen for its flexibility and prowess in handling text/data cleaning up tasks.

​	The implementation is quite straightforward. To ensure scalability, two abstract classes (interfaces) were introduced, the "RuleEngine" and "SignalStream", from which all customized engines and streams should derive (details can be referred to in the docstring). The "SignalProcessor" takes in any objects (classes) that implements these pre-defined interfaces, runs them with multi-threading so that the program will not be frozen waiting for I/O, and calls a call-back function (can be a machine learning sub-routine) after a signal item is processed. Since the program utilizes metaclasses, <u>it requires Python 3.x to run</u>.

​	The current implementation of SignalProcessor and the JSON engines/signalstream didn't consider competing situations and dead-locks because it is assumed that a processor only works with one rule engine to process a specific signal stream. This is the case when rules and signal streams are small local files and can be simply cached as an entirety. However, if, for example, rules are loaded from remote servers and multiple rules needs to be applied to the same signal streams, more delicacy is needed. Mutexes can be used to lock up the resources, but the signal processor needs to make sure the atomicity of operations to avoid competing situations.

​	By using multi-threading, the program should have obtained very good performance. However, due to the Global Interpreter Lock of CPython, multi-threading is not as efficient as in other languages. One choice is, of course, to completely switch to other languages, such as Java or C++. Another choice is to use a new feature - asyncio, introduced in Python 3.4, to automatically switch among tasks when there is a blocking I/O operation, to mimic multi-threading in a single-threaded program. This will give better performance as there will be no context-switching as with multi-threading, but will require additional work to implement atomic I/O operations for each specific signal source so that the control of program flow will be "yielded" to the event loop while waiting for further inputs.

​	Another way to improve performance is to cache the signal stream and process the cached signals with rule engine in batches. This could be very useful when the signal source needs some time to "boot" and "shutdown" before getting a signal, and cannot be always on.



**Folder Structure**

│  raw_data.json					Test signal input file.
│  readme.md					This file.
│  rules.json						Test rule input file.
│  rules_engine.py				Main execution file.
│                                                 

├─signal_filter					Signal filter module.
│  │  dummy.py					Dummy rule engine and signal stream for testing.
│  │  interface.py					Abstract classes that outlines how rule engines and signal streams should be implemented.
│  │  JSONFileRuleEngine.py		A rule engine that reads rules from a JSON file.
│  │  JSONFileSignalStream.py		A signal stream that reads signals from a JSON file.
│  │  SignalProcessor.py			The signal processor that matches signal streams and rule engines together.
│  │  \__init__.py					The module init file.
│                                             

└─unit_test						Python unit test module.



**JSON Rules File Definition**

The current implementation of JSONFileRuleEngine reads in a JSON rule file. The format is defined in a very similar fashion to the JSON signal inputs file. There is only one additional key "op", which is the operator used to compare with the signal inputs. 

Currently, the following operators are supported (same as in C-alike languages):

==, >, <, !=

For value type of "datetime", in the key "value", a built-in function "TODAY" was implemented to get the current datetime. An example is shown as follows:

{ "signal": "ATL1", "op": "<=", "value": "TODAY", "value_type": "Datetime"}

This filters out all value from ATL1 where the datetime is in the future.





**-END-**

