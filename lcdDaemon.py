#!/usr/bin/env python
import logging, time, os, sys
from daemon import runner #pip install python-daemon

# add paths for base and command objects
app_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(app_dir + '/base')
sys.path.append(app_dir + '/commands')

from CommandRunner import CommandRunner
from Command import Command

class DaemonLCD:
	def __init__(self): 
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'
		self.stderr_path = '/dev/null'
		self.pidfile_path =  '/var/run/lcdDaemon.pid'
		self.pidfile_timeout = 5
	
	def run(self):
		# Load configs
		screen_type = Command().loadConfig('screen')
		commands_config = Command().loadConfig('commands')
		images_config = Command().loadConfig('images')
		
		
		# Get list of commands to run (exclude commands including them in config.yml)
		avaliable_commands = []
		for command_file in os.listdir(app_dir + '/commands'):
			if command_file.endswith(".py"): 
				command_name = os.path.splitext(command_file)[0] 
				if command_name not in commands_config['exclude']:
					avaliable_commands.append(command_name)
				else:
					logger.debug('Skiped command ' + command_name)
		
		avaliable_commands.sort()
		
		# Get list of avaliable images (exclude images including them in config.yml)
		avaliable_images= []
		for image in os.listdir(app_dir + '/images'):
			if image.endswith(".bmp") or image.endswith(".png"):
				if image not in images_config['exclude']:
					avaliable_images.append(image)
				else:
					logger.debug('Skiped image ' + image)
		
		avaliable_images.sort()
		
		#instance screen object
		try:
			module = __import__('Screen')
			class_ = getattr(module, screen_type)
			screen = class_()
		except:
			logger.error("Error loading screen control for " + screen_type + ". lcdDaemon finished!")
			sys.exit(1)
		
		# Turn off led light
		screen.ledLight(0)

		while True:
			# Run info commands
			for command in avaliable_commands:
				command_runner = CommandRunner(command)
				command_runner.instance()
				output = command_runner.launchCommand()
				logger.debug(output)
				screen.screenMessage(output)
				time.sleep(commands_config['sleep'])
			
			#Load screen images
			for image in avaliable_images: 
				image_to_screen = app_dir + '/images/' + image
				logger.debug("LOAD: " + image_to_screen)
				screen.loadImage(image_to_screen)
				time.sleep(images_config['sleep'])


lcd_daemon_app = DaemonLCD()
logger = logging.getLogger("lcd-daemon")
logger.setLevel(logging.INFO) #Set to logging.DEBUG while debugging 
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler('/var/log/lcdDaemon.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

lcd_daemon_runner = runner.DaemonRunner(lcd_daemon_app)
# Avoid clossing log file
lcd_daemon_runner.daemon_context.files_preserve=[handler.stream]
lcd_daemon_runner.do_action()
