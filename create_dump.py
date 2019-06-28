import pexpect
import sys
import os
from subprocess import PIPE, call, Popen
import subprocess
from datetime import datetime

# Change environment variable to powershell on windows

os.environ['COMSPEC'] = 'powershell'
<<<<<<< HEAD
=======
password = 'smart'
user = 'root'
database = 'tracking'
>>>>>>> dc16f00df91d7a1e4f784f68da7f6d5828e021da

def count():
	date_time = datetime.now()
	today = date_time.strftime("%m-%d-%Y-%H-%M-%S")
	return today

def backup():
	'''Backup to a *.sql file'''
	today = count()
	backup_name = "backup"+today+".sql"

<<<<<<< HEAD
	try:
		with open(backup_name, 'w') as backup_file:
			password = 'smart'
			user = 'root'
			database = 'tracking'
			
			cmd=('mysqldump -u root -p tracking tbl_cars cars_status -r "%s"'%backup_name)

			child = pexpect.spawn(cmd)
			# child.logfile_read = sys.stdout.buffer
			i = child.expect([pexpect.TIMEOUT, "Enter password:"])

			if i == 0:
				print("Got unexpected output: %s %s" % (child.before, child.after))
				sys.exit()
			else:
				try:
					child.sendline(password)
					child.sendline('exit')
					child.expect(pexpect.EOF)
				except:
					print('didnt pass password')

	except:
		print('failed to create file')
=======
	# with open(backup_name) as backup_file:
	process = Popen([r'mysqldump', '-u', 'root', '-psmart', 'tracking', 'tbl_cars','cars_status'], stdin=PIPE, stderr=PIPE, stdout=open(backup_name, 'w+'), shell=True)
	process.communicate()
>>>>>>> dc16f00df91d7a1e4f784f68da7f6d5828e021da
