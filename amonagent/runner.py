from amonagent.collector import (
	get_memory_info,
	get_cpu_utilization,
	get_process_list,
	get_disk_check,
	get_network_traffic,
)
from amonagent.distro import windows_platform_data
from amonagent.collector import NetIOCounters

class Runner(object):

	def info(self):
		return windows_platform_data()

	def system(self):
		net = NetIOCounters()
		
		system_data_dict = {
			'memory': get_memory_info(),
			'cpu': get_cpu_utilization(),
			'disk': get_disk_check(),
			'network': net.result(),
		}
		return system_data_dict


	def processes(self):
		return get_process_list()

runner = Runner()
