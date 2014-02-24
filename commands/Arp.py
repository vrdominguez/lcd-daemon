from Command import Command
import logging

class Arp(Command):
	'Check router arp table'
	def runCommand(self):
		config = self.loadConfig('router') 
		
		#Load router specific class
		module = __import__('Router')
		router_class = getattr(module, config['class'])
		
		router = router_class(config['user'], config['password'])
		
		return self.checkMacList(self.getLanMacs(router.getArpTable()))
		
	def getLanMacs(self, arp_table):
		lan = []
			
		for entry in arp_table:
			data = entry.split()
			
			# Only br0 (lan) and no 00:00...:00 mac	devices
			if (data[3] == '00:00:00:00:00:00') or (data[5] != 'br0'):
				continue
			
			lan.append({'mac':data[3],'ip':data[0]})
		
			
		return lan 
	
	def checkMacList(self, lan_arp):
		# Load every time in case we add more known Macs
		macs = self.loadConfig('macs')
		
		conected_devices = len(lan_arp)
		unknown_devices = []
		
		for mac_data in lan_arp:
			if mac_data['mac'] not in macs:
				unknown_devices.append(mac_data)
			
		unknown_count = len(unknown_devices)
		
		if unknown_count:
			# Get access to log file
			logger = logging.getLogger("lcd-daemon")
			
			# Only try to log the unknown devices if a log handler is defined 
			if len(logger.handlers):
				for data in unknown_devices:
					logger.warning('Unknown device detected. MAC: ' + data['mac'])
		
		return ['  ARP  TABLE', '--------------', 'Conected: ' + str(conected_devices), 'Known: ' + str(conected_devices - unknown_count), 'Unknown: ' + str(unknown_count)] 
