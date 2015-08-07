import os
import sys
import ConfigParser

def ConfigSectionMap(section):
	dict1 = {}
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == -1:
				print("skip: %s" % option)
		except:
			print("Option not found %s!" % option)
			dict1[option] = None
	return dict1


config_name = 'amon-agent.ini'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config = {}
try:
	config_path = os.path.join(application_path, config_name)
	Config = ConfigParser.ConfigParser()
	Config.read(config_path)
except Exception, e:
	print "There was an error in your configuration file ({0})".format(config_path)

config_values = {}
try:
	config_values = ConfigSectionMap("Main")
except Exception, e:
	print "There was an error reading section Main in your configuration file ({0})".format(config_path)

# 1 minute default
SYSTEM_CHECK_PERIOD = config_values.get('system_check_period', 60)
HOST = config_values.get('amon_url')
SERVER_KEY = config_values.get('server_key', None)