#lcdDaemon - Test All commands One Liner
To test all the implemented commands, you can run this one liner

```bash
find commands/ -iname '*.py' | awk -F '/' '{print $2}' | sort | awk -F '.' '{print "echo Command "$1":; python test.py "$1"; echo;"}' | sh
```
Example
================
This is an example of the test output:

```
root@tardis:/home/lcd-daemon# find commands/ -iname '*.py' | awk -F '/' '{print $2}' | sort | awk -F '.' '{print "echo Command "$1":; python test.py "$1"; echo;"}' | sh
Command Adsl:
['  ADSL STATUS', '--------------', '- Upstream:', '943 Kbps', '- Downstream:', '7952 Kbps']

Command Disk:
['  DISK USAGE', '--------------', 'Used: 647G', 'Free: 1,1T', 'Total: 1,8T']

Command Ip:
['Network IP(s):', '--------------', '', '***.***.***.***', '', '***.***.***.***']

Command Load:
[' LOAD AVERAGE ', '--------------', '  1 m: 0.49', '  5 m: 0.47', ' 15 m: 0.24']

Command Ram:
['  RAM  USAGE', '--------------', 'Total: 485 MB', 'Used: 362 MB', 'Free: 123 MB']

Command Temperature:
['  TEMPERATURE', '--------------', '', "    47.1'C", '', '']

Command Uptime:
['    UPTIME', '--------------', 'Days: 0', 'Hours: 0', 'Minutes: 4']

root@tardis:/home/lcd-daemon#
```
