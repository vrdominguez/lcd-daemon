from nokiaSPI import NokiaSPI
import os, time

class NokiaLCD:
	def __init__(self):
		self.lines = 6
		self.line_len = 14
		self.empty_line = '              '
		self.control = NokiaSPI()
		self.control.cls()
	
	def loadImage(self, image_path='/home/lcd-daemon/images/raspi.bmp', line=''):
		if os.path.isfile(image_path):
			self.control.load_bitmap(image_path, True)
			if len(line) > 0:
				if line.len() > 14:
					raise ValueError('Image message to long')
				else:
					self.control.text(line)
		else:
			self.control.cls()
			self.control.text('IMG ERROR 404:')
			self.control.text(self.empty_line)
			self.control.text('The image was ')
			self.control.text('not found...  ')
			self.control.text(self.empty_line)
			self.control.text(self.empty_line)
			# IOError
			raise IOError('Image "' + image_path + '" not found')
	
	def screenMessage(self, message=[], wait=1):
		message_lines = len(message)
		
		if message_lines < 1:
			raise ValueError('Empty message')
		else:
			# Message validation
			for num_line in range(0,message_lines):
				if len(message[num_line]) > self.line_len:
					raise ValueError("Line " + str(num_line) + " is too long")
		
		#Message printing
		self.control.cls()
		count = 1	
		for line in message:
			if count > self.lines:
				time.sleep(wait)
				self.control.cls()
				count = 1
			
			while len(line) < self.line_len:
				line += ' '
			
			self.control.text(line)
			count = count + 1
	
	def ledLight(self,power=1):
		if power > 0:
			for i in range(0,255):
				self.control.led(i)
				time.sleep(0.025)
			self.control .led(255)
			
		else:
			for i in range(255,0,-1):
				self.control.led(i)
				time.sleep(0.025)
			self.control .led(0)
