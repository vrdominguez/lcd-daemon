lcdDaemon
================
Python daemon which shows system info using the Nokia LCD screen sold by Texy at [Raspberry Pi forums](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=93&t=14913)

nokiaSPY was created by bgreat from the [Raspberry Pi forums](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=9814&p=262274&hilit=nokiaSPI)

Instructions
------------
 - Put the code in /home/lcd-daemon (or any other place you like)
 - Grab [nokiaSPI code](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=9814&p=262274&hilit=nokiaSPI) and put it into "./base/"
 - Copy config.yml-dist to config.yml and edit it as needed
 - Create an init.d script [(Example)](https://gist.github.com/vrdominguez/8958308)
 - Start the daemon with "service lcd-daemon start", where lcd-daemon stands for your init.d script

Autostart at system startup:
------------
As root, add the init.d script to rc with update-rc.d: update-rc.d lcd-daemom defaults 

Notes
------------
At this moment, only Vodafone HG556a is supported for ADSL data and public IP grab, you can add your own router to base/Router.py (you can add Ip and Adsl to excluded commands at config.yml for a quick test of the daemon)
