import pexpect
import sys
import os
from subprocess import PIPE, call, Popen
import subprocess
from datetime import datetime

# Change environment variable to powershell on windows

# os.environ['COMSPEC'] = 'powershell'

password = ''
user = 'root'


def count():
	date_time = datetime.now()
	today = date_time.strftime("%m-%d-%Y-%H-%M-%S")
	return today

def backup(db_name):
	'''Backup to a *.sql file'''
	today = count()
	backup_name = "backup"+today+".sql"

	try:
		process = Popen([r'mysqldump', '-u', 'root', '-psmart', 'tracking', 'tbl_cars','cars_status'], stdin=PIPE, stderr=PIPE, stdout=open(backup_name, 'w+'), shell=True)
		process.communicate()
	except:
		print('Mysql operation failed')








	# with open(backup_name, 'w') as backup_file:
	# 		password = ''
	# 		user = 'root'
	# 		db = str(db_name)
	# 		print("working on :",db)
			
	# 		cmd=('mysqldump -u root -p "%s" tbl_cars cars_status -r "%s"'%(db, backup_name))
	# 		print(cmd)

	# 		child = pexpect.spawn(cmd)
	# 		child.logfile_read = sys.stdout.buffer
	# 		i = child.expect([pexpect.TIMEOUT, "Enter password:"])
	# 		print(i)

	# 		if i == 0:
	# 			print("Got unexpected output: %s %s" % (child.before, child.after))
	# 			sys.exit()
	# 		else:
	# 			try:
	# 				child.sendline(password)
	# 				child.sendline('exit')
	# 				child.expect(pexpect.EOF)
	# 			except:
	# 				print('password not passed')
