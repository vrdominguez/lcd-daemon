#!/usr/bin/env python
# Use this file to test your command output
# Usage: ./test.py <your_command>
import os, sys, argparse

# Aditional app paths
app_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(app_dir + '/base')
sys.path.append(app_dir + '/commands')

# Get list of avaliable commands 
avaliable_commands = []
for command_file in os.listdir(app_dir + '/commands'):
	if command_file.endswith(".py"):
		avaliable_commands.append(os.path.splitext(command_file)[0])

avaliable_commands.sort()

# Command help text with avaliable commands
command_help = "Command to run. Avaliable commands: " + ", ".join(avaliable_commands)

# Parse Arguments 
parser = argparse.ArgumentParser()
parser.add_argument("command", help=command_help)
args = parser.parse_args()

launched_command = args.command

# Fromating the command name correctly 
instance_command = launched_command.lower().capitalize()

if instance_command in avaliable_commands:
	# Instance the command
	try:
		module = __import__(instance_command)
		class_ = getattr(module, instance_command)
		command= class_()
		
	except:
		print "Error loading the command '" + launched_command + "'"
		sys.exit(1)
	
	try:
		print command.runCommand()
	except: 
		print "Error executing", launched_command
		sys.exit(1)
else:
	print 'Command "' + launched_command + '" not avaliable'
	print "Avaliable commands \n\t- " + "\n\t- ".join(avaliable_commands)
	sys.exit(1)
