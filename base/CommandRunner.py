class CommandRunner:
	def __init__(self,command):
		self.command = command
	
	def instance(self):
		instance_command = self.command.lower().capitalize()
		
		# Instance the command	
		module = __import__(instance_command)
		class_ = getattr(module, instance_command)
		self.command_object = class_()
	
	def launchCommand(self):
		# Run the command
		return self.command_object.runCommand()
