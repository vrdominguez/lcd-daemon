from Command import Command
import subprocess as s

class Temperature(Command):
	'Get system uptime'
	def runCommand(self):
		temp = s.Popen(['/usr/bin/vcgencmd','measure_temp'] , stdout=s.PIPE, stderr=s.PIPE).communicate()[0].split("\n")[0].split('=')
		return ['  TEMPERATURE','--------------', '', '    '+temp[1],'','']
