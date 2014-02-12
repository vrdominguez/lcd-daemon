import os,sys,yaml

class Command:
	'Base class for comands'
	def getBaseDir(self):
		return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/..')
	
	def loadConfig(self, config):
		config_file_path = self.getBaseDir()+'/config.yml'	
		config_file = open(config_file_path)
		config_data = yaml.safe_load(config_file)
		return config_data[config]
	
	def runCommand(self):
		raise NotImplementedError('Must be implemented for your command')
