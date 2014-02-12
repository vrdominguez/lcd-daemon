from Command import Command
import subprocess as s
import re

class Ip(Command):
	'Get router ip'
	def runCommand(self):
		return ['Network IP(s):','--------------', '', self.getRouterIp(), '', self.getNetworkIp()]
	
	
	def getNetworkIp(self, device='eth0'):
		data = [line.strip() for line in s.Popen(['ifconfig', device], stdout=s.PIPE, stderr=s.PIPE).communicate()[0] .split("\n") if line.strip()]
		
		regexp_ip = re.compile('^inet\s+addr:((\d{1,3}\.){3}\d{1,3}).+',re.IGNORECASE)
		
		for line in data:
			data = regexp_ip.match(line)
			if (data):
				return data.group(1)
		return 'unknown'
	
	def getRouterIp(self):
		config = self.loadConfig('router') 
		
		#Load router specific class
		module = __import__('Router')
		router_class = getattr(module, config['class'])
		router = router_class(config['user'], config['password'])
		
		return router.getPublicIp()
