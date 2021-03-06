from Command import Command
import subprocess as s

class Uptime(Command):
	'Get system uptime'
	def runCommand(self):
		uptime = s.Popen(['/usr/bin/uptime'] , stdout=s.PIPE, stderr=s.PIPE).communicate()[0].split("\n")[0].replace(",","").split()
		
		if uptime[3] == 'day' or uptime[3] == 'days':
			if uptime[5] == 'min':
				return ['    UPTIME', '--------------', 'Days: ' + uptime[2], 'Hours: 0', 'Minutes: ' + uptime[4]]
			else:
				time = uptime[4].split(':')
				return ['    UPTIME', '--------------', 'Days: ' + uptime[2], 'Hours: ' + time[0], 'Minutes: ' + time[1]]
		elif uptime[3] == 'min':
			return ['    UPTIME', '--------------', 'Days: 0', 'Hours: 0',  'Minutes: ' + uptime[2]]
		else:
			time = uptime[2].split(':')
			return ['    UPTIME', '--------------', 'Days: 0', 'Hours: ' + time[0], 'Minutes: ' + time[1].split(',')[0]]
