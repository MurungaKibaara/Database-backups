import pexpect
import sys
import json
import os
import re
import argparse
from subprocess import PIPE, call, Popen
import subprocess
from datetime import datetime

def count():
	'''Create date format to add to name string'''
	date_time = datetime.now()
	today = date_time.strftime("%m-%d-%Y-%H-%M-%S")
	return today

def backup(database, user, ip, password, tables):
	'''Backup to a *.sql file'''

	for db in database:
		for users in user:
			for passwd in password:
				for host in ip:
					tbls = json.dumps(tables).strip('[]')
					print(tbls)

					today = count()
					backup_name = "backup"+today+".sql"
					try:
						for table in tables:
							cmd=[r'mysqldump', '-h', host, '-u', users, '-p{}'.format(passwd), '%s'%db, table]
							print(cmd)
							process = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=open(backup_name, 'a'), shell=True)
							process.communicate()
					except:
						print('Mysql operation failed')

tables = ['cars', 'tbl_cars', 'cars_status']
database = ['tracking']
ip = ["localhost"]
user = ["root"]
password = [""]

backup(database, user, ip, password, tables)







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

# for db in database:
# 	tbls = ','.join(tables)
# 	# tbls = str(tables).split("[]")
# 	print(str(tbl1))
# 	# print(db, tbls)

