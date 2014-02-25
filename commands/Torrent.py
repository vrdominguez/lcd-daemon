from Command import Command
from transmission import Transmission # pip install transmission-fluid

class Torrent(Command):
	'Get transmission stats'
	def runCommand(self):
		config = self.loadConfig('transmission');
		client = Transmission(username=config['user'], password=config['passwd'])
		response = client('session-stats')
		
		return [' TRANSMISSION','--------------','Acive: ' + str(response['activeTorrentCount']),'Speeds (kbps)','- Up:' + str(response['uploadSpeed']/1024),'- Down:' + str(response['downloadSpeed']/1024)]
