from Command import Command
import commands
import subprocess as s

class Load(Command):
	'System load'
	
	def runCommand(self):
		#load = commands.getoutput("cat /proc/loadavg")
		load = s.Popen(['cat', '/proc/loadavg'] , stdout=s.PIPE, stderr=s.PIPE).communicate()[0]
		data = load.split(" ")
		return [' LOAD AVERAGE ', '--------------', '  1 m: '+data[0], '  5 m: '+data[1], ' 15 m: '+data[2]]
