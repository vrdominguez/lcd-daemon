from Command import Command
import subprocess as s

class Disk(Command):
	'Get disk usage'
	def runCommand(self):
		disk = self.loadConfig('disk')
		disk_usage = self.getDiskUsage(disk)
		return [ '  DISK USAGE', '--------------', 'Used: ' + disk_usage[2], 'Free: ' + disk_usage[3], 'Total: ' + disk_usage[1]]
	
	def getDiskUsage(self,disk):
		data = s.Popen(['/bin/df', '-h', disk], stdout=s.PIPE, stderr=s.PIPE).communicate()[0] .split("\n")[1] 
		return data.split()
