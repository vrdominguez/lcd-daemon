from Command import Command
import subprocess as s
import re

class Cpu(Command):
	'Get CPU usage'
	def runCommand(self):
		#cpu = s.Popen('/usr/bin/mpstat | grep -A2  "%idle" | tail -n 1 | awk -F " " "{print 100 - $11}"a', shell=True, stdout=s.PIPE, stderr=s.PIPE).stdout.read().rstrip()
		cpu = s.Popen('/usr/bin/mpstat | grep -A2  "%idle" | tail -n 1', shell=True, stdout=s.PIPE, stderr=s.PIPE).stdout.read().rstrip()
		cpu_idle = float(cpu.split()[10].replace(',','.'))
		cpu = 100 - cpu_idle	
		return ['  CPU  USAGE', '--------------','', '   ' + "{:0.2f}".format(cpu) + ' %']
