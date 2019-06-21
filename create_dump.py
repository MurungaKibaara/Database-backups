import pexpect
import sys
import os
from datetime import datetime

# Change environment variable to powershell on windows

# os.environ['COMSPEC'] = 'powershell'

def count():
	date_time = datetime.now()
	today = date_time.strftime("%m-%d-%Y-%H-%M-%S")
	return today

def backup():
	'''Backup to a *.sql file'''
	today = count()
	backup_name = "backup"+today+".sql"

	try:
		with open(backup_name, 'w') as backup_file:
			password = ''
			user = 'root'
			database = ''
			
			cmd=('mysqldump -u root -p tracking2 tbl_cars cars_status -r "%s"'%backup_name)

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
