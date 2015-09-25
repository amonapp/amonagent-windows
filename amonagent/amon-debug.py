#!/usr/bin/python
import logging
import sys, time
import os.path
import json

if __package__ is None and not hasattr(sys, "frozen"):
    # It is a direct call to __main__.py
    
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(path)))

try:
	import amonagent
except:
	print 'amonagent is not installed'
	sys.exit()

from amonagent.runner import runner
from amonagent.collector import get_network_traffic
if __name__ == "__main__":
	stats = {
		'info': runner.info(),
		'system': runner.system(),
		'processes': runner.processes(),
		'network_raw': get_network_traffic()
	}

	with open('amon-debug.json', "w+") as file:
		json.dump(stats, file, indent=4)
