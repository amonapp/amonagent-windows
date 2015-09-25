#!/usr/bin/python
import logging
import sys, time
import os.path

if __package__ is None and not hasattr(sys, "frozen"):
    # It is a direct call to __main__.py
    
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(path)))

try:
	import amonagent
except:
	print 'amonagent is not installed'
	sys.exit()

from amonagent import __version__
from amonagent.runner import Runner
from amonagent.remote import Remote
from amonagent.settings import settings 

if __name__ == "__main__":
	remote = Remote()
	runner = Runner()
	remote.save_system_info(runner.info())

	while True:
		runner = Runner()
		stats = {
			'system': runner.system(),
			'processes': runner.processes(),
		}
		remote.save_system_stats(stats)
		time.sleep(settings.SYSTEM_CHECK_PERIOD)