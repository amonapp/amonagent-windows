import psutil
import logging
import time
import netifaces
import wmi

log = logging.getLogger(__name__)
c = wmi.WMI()

size_list = [
	(1024 ** 5, 'PB'),
	(1024 ** 4, 'TB'), 
	(1024 ** 3, 'GB'), 
	(1024 ** 2, 'MB'), 
	(1024 ** 1, 'KB'),
	(1024 ** 0, ('byte', 'bytes')),
]

def convert_bytes_to(value, to='MB'):
	for factor, suffix in size_list:
		if suffix == to:
			break
	try:
		value = float(value/factor)
		value = round(value)
	except:
		pass

	return value

def convert_dict_from_bytes(dict_to_convert, except_list=None, to='MB'):
	for k, v in dict_to_convert.items():
		if k not in except_list:
			dict_to_convert[k] = convert_bytes_to(v, to=to)

	return dict_to_convert

def get_memory_info():
	memory_dict = {}
	virtual_memory = psutil.virtual_memory()
	swap_memory = psutil.swap_memory()

	memory_dict = {
			"total_mb": virtual_memory.total,
			"free_mb": virtual_memory.free,
			"used_mb": virtual_memory.used,
			"used_percent": virtual_memory.percent,
			"swap_total_mb":swap_memory.total,
			"swap_free_mb": swap_memory.free,
			"swap_used_mb": swap_memory.used,
			"swap_used_percent": swap_memory.percent
	}
	memory_dict = convert_dict_from_bytes(memory_dict,
		except_list=['used_percent', 'swap_used_percent'])


	return memory_dict


def get_disk_check():
	volumes = {}

	_volume_columns = ('total', 'used', 'free', 'percent')
	for disk in c.Win32_LogicalDisk(DriveType=3):
		disk_info =  psutil.disk_usage(disk.DeviceID)
		volume = {}
		volume_values =  dict(zip(_volume_columns, disk_info))
		volumes[disk.DeviceID] = convert_dict_from_bytes(volume_values,
			except_list=['percent', 'name'], to='GB')

	return volumes


def get_network_traffic():
	data = {}
	result = psutil.net_io_counters(pernic=True)
	for interface, value in result.items():
		data[interface] = {
			"inbound": convert_bytes_to(value.bytes_recv, to='KB'),
			"outbound": convert_bytes_to(value.bytes_sent, to='KB')
		}

	return data


def get_cpu_utilization():
	data = {}
	cpu_times_percent = psutil.cpu_times_percent(interval=1)
	for stat in ['user', 'system', 'idle']:
		if hasattr(cpu_times_percent, stat):
			data[stat] = getattr(cpu_times_percent, stat)
		

	return data

def get_process_list():

	process_data = {}
	attrs=['pid', 'name', 'io_counters', 'memory_info', 'cpu_percent', 'cpu_times']

	for proc in psutil.process_iter():

		try:
			pinfo = proc.as_dict(attrs=attrs)
		except psutil.NoSuchProcess:
			pinfo = None

		try:
			name = proc.name()
		except:
			name = None
		
		try:
			memory_info =  proc.memory_info()
			memory_bytes = memory_info.rss
		except:
			memory_bytes = 0

		process_data[name] = {
			"cpu": proc.cpu_percent(interval=0.1),
			"memory_mb": convert_bytes_to(memory_bytes),
			"kb_read": convert_bytes_to(pinfo['io_counters'].read_bytes),
			"kb_write": convert_bytes_to(pinfo['io_counters'].write_bytes),
		}

	return process_data


class NetIOCounters(object):
	def __init__(self, pernic=True):
		self.last_req = None
		self.last_req_time = None
		self.pernic = pernic

	def _get_net_io_counters(self):
		"""
		Fetch io counters from psutil and transform it to
		dicts with the additional attributes defaulted
		"""
		counters = psutil.net_io_counters(pernic=self.pernic)

		res = {}
		for name, io in counters.iteritems():
			res[name] = io._asdict()
			res[name].update({'tx_per_sec': 0, 'rx_per_sec': 0})
		return res

	def _set_last_request(self, counters):
		self.last_req = counters
		self.last_req_time = time.time()

	def get(self):
		return self.last_req

	def update(self):
		counters = self._get_net_io_counters()

		if not self.last_req:
			self._set_last_request(counters)
			return counters

		time_delta = time.time() - self.last_req_time

		if not time_delta:
			return counters

		for name, io in counters.iteritems():
			last_io = self.last_req.get(name)
			if not last_io:
				continue

			counters[name].update({
				'inbound': (io['bytes_recv'] - last_io['bytes_recv']) / time_delta,
				'outbound': (io['bytes_sent'] - last_io['bytes_sent']) / time_delta
			})


		self._set_last_request(counters)

		return counters

	def result(self):
		data = {}
		self.update()
		result = self.update()
		for iface, values in result.items():
			inbound = values.get('inbound', 0)
			outbound = values.get("outbound", 0)
			data[iface] = {
				'inbound': convert_bytes_to(inbound, to='KB'),
				'outbound': convert_bytes_to(outbound, to='KB')
			}
			
		return data


def get_interface_addresses():
	"""
	Get addresses of available network interfaces.
	See netifaces on pypi for details.
	Returns a list of dicts
	"""

	addresses = []
	ifaces = netifaces.interfaces()
	for iface in ifaces:
		addrs = netifaces.ifaddresses(iface)
		families = addrs.keys()

		# put IPv4 to the end so it lists as the main iface address
		if netifaces.AF_INET in families:
			families.remove(netifaces.AF_INET)
			families.append(netifaces.AF_INET)

		for family in families:
			for addr in addrs[family]:
				address = {
					'name': iface,
					'family': family,
					'ip': addr['addr'],
				}
				addresses.append(address)

	return addresses


# net = NetIOCounters()
# print net.result()
system_data_dict = {
	# 'memory': get_memory_info(),
	# 'cpu': get_cpu_utilization(),
	# 'disk': get_disk_check(),
	# 'network': get_network_traffic(),
	# 'processes': get_process_list()
}

# print system_data_dict