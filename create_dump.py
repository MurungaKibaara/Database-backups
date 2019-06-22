import pexpect
import sys
import os
from subprocess import PIPE, call, Popen
import subprocess
from datetime import datetime

# Change environment variable to powershell on windows

os.environ['COMSPEC'] = 'powershell'
password = 'smart'
user = 'root'
database = 'tracking'

def count():
	date_time = datetime.now()
	today = date_time.strftime("%m-%d-%Y-%H-%M-%S")
	return today

def backup():
	'''Backup to a *.sql file'''
	today = count()
	backup_name = "backup"+today+".sql"

	# with open(backup_name) as backup_file:
	process = Popen([r'mysqldump', '-u', 'root', '-psmart', 'tracking', 'tbl_cars','cars_status'], stdin=PIPE, stderr=PIPE, stdout=open(backup_name, 'w+'), shell=True)
	process.communicate()
