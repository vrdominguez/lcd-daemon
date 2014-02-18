from Command import Command
import subprocess as s

class Ram(Command):
	'Get RAM status'
	def runCommand(self):
		ram_status = s.Popen(['/usr/bin/free', '-m'] , stdout=s.PIPE, stderr=s.PIPE).communicate()[0].split("\n")[1].split()
		return ['  RAM  USAGE', '--------------','Total: ' + ram_status[1] + ' MB', 'Used: ' + ram_status[3] + ' MB', 'Free: ' + ram_status[2] + ' MB']
