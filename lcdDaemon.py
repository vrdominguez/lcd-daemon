#!/usr/bin/env python
import logging, time, os, sys
from daemon import runner #pip install python-daemon

# add paths for base and command objects
app_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(app_dir + '/base')
sys.path.append(app_dir + '/commands')

from Command import Command, CommandRunner

class DaemonLCD:
	def __init__(self): 
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'
		self.stderr_path = '/dev/null'
		self.pidfile_path =  '/var/run/lcdDaemon.pid'
		self.pidfile_timeout = 5
		self.running = 0
	
	def run(self):
		logger.info("lcdDaemon started!")
		self.running = 1
		
		# Load configs
		screen_type = Command().loadConfig('screen')
		commands_config = Command().loadConfig('commands')
		images_config = Command().loadConfig('images')
		led_power = Command().loadConfig('led')
		
		
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
			self.screen = class_()
		except:
			self.running = 0
			logger.error("Error loading screen control for " + screen_type + ". lcdDaemon finished!")
			sys.exit(1)
		try:
			self.screen.loadImage( app_dir + '/images/' + Command().loadConfig('splash') )
		except Exception as e:
			logger.error("Error showing splash image: " + str(e))
		
		# Turn off led light (if required)
		if not led_power:
			logger.debug('Turnin off led light')
			self.screen.ledLightProgressive(0)
		else:
			time.sleep(5)

		while True:
			# Run info commands
			for command in avaliable_commands:
				try:
					command_runner = CommandRunner(command)
					command_runner.instance()
					output = command_runner.launchCommand()
					logger.debug(output)
					self.screen.screenMessage(output)
					time.sleep(commands_config['sleep'])
				except Exception as e:
					logger.error("Error executing '" + command + "': " + str(e))
			
			#Load screen images
			for image in avaliable_images: 
				try:
					image_to_screen = app_dir + '/images/' + image
					logger.debug("LOAD: " + image_to_screen)
					self.screen.loadImage(image_to_screen)
					time.sleep(images_config['sleep'])
				except Exception as e:
					logger.error("Error loading image '" + image + "': " + str(e))

	def __del__(self):
		if self.running:
			self.screen.clear()
			self.screen.ledLight(0)
			self.led_power = 0
			self.running = 0
			logger.info('Daemon finished')


logger = logging.getLogger("lcd-daemon")
logger.setLevel(logging.INFO) #Set to logging.DEBUG while debugging 
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler('/var/log/lcdDaemon.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

lcd_daemon_app = DaemonLCD()
lcd_daemon_runner = runner.DaemonRunner(lcd_daemon_app)
# Avoid clossing log file
lcd_daemon_runner.daemon_context.files_preserve=[handler.stream]
lcd_daemon_runner.do_action()
