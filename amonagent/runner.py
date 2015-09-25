from amonagent.collector import (
	get_memory_info,
	get_cpu_utilization,
	get_process_list,
	get_disk_check,
	get_network_traffic,
)
from amonagent.distro import windows_platform_data

class Runner(object):

	def info(self):
		return windows_platform_data()

	def system(self):
		
		system_data_dict = {
			'memory': get_memory_info(),
			'cpu': get_cpu_utilization(),
			'disk': get_disk_check(),
			'network': get_network_traffic(),
		}
		return system_data_dict


	def processes(self):
		return get_process_list()

runner = Runner()
