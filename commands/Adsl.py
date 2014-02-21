from Command import Command

class Adsl(Command):
	'Check adsl status'
	def runCommand(self):
		config = self.loadConfig('router') 
		
		#Load router specific class
		module = __import__('Router')
		router_class = getattr(module, config['class'])
		
		router = router_class(config['user'], config['password'])
	
		output = router.getConnectionStatus()
		
		return ['  ADSL STATUS', '--------------', '- Upstream:', output[1], '- Downstream:', output[2]]
