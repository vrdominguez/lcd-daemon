from Command import Command
import subprocess as s
import re

class Dinaip(Command):
	'Get dinaIP service status'
	def runCommand(self):
		service_data = self.getServiceStatus() 
		return ['DINAIP ' + service_data[0],'--------------','- Domain:',service_data[1],'- Subdomain:', service_data[2] ]
	
	def getServiceStatus(self):
		data = [line.strip() for line in s.Popen(['/usr/sbin/service', 'dinaip', 'status'], stdout=s.PIPE, stderr=s.PIPE).communicate()[0] .split("\n") if line.strip()]

		status = 'STOPPED'
		if data[0].split(' ')[2] == '[si]':
			status = 'STARTED'
		
		domain = 'Not defined'
		zone = 'Not defined'
			
		if data[3]:
			tmp_array =data[3].split(' ')
			domain = tmp_array[1]
			zone = tmp_array[3]
		
			
		return [status, domain, zone] 
