from Command import Command
from transmission import Transmission # pip install transmission-fluid
import subprocess as s

class Torrent(Command):
	'Get transmission stats'
	def runCommand(self):
		
		# Check if transmission is running
		transmission_status = s.Popen(['/usr/sbin/service', 'transmission-daemon', 'status'] , stdout=s.PIPE, stderr=s.PIPE).communicate()[0].split("\n")[0]
		
		if transmission_status == 'transmission-daemon is running.':
			config = self.loadConfig('transmission');
			client = Transmission(username=config['user'], password=config['passwd'])
			response = client('session-stats')
			
			return [' TRANSMISSION','--------------','Active: ' + str(response['activeTorrentCount']),'Speeds (KB/s)','- Up: ' + str(response['uploadSpeed']/1024),'- Down: ' + str(response['downloadSpeed']/1024)]
		
		else:
			return [' TRANSMISSION','--------------','', ' NOT RUNNING!']
