import pexpect
import sys
from subprocess import PIPE, call, Popen
from registry import get_reg
from datetime import datetime

def count():
	'''Create date format to add to name string'''
	date_time = datetime.now()
	today = date_time.strftime("%m-%d-%Y-%H-%M-%S")
	return today

def get_registry_values():
	'''Get values from registry and post them in the backup function'''
	try:
		tables = get_reg('tables')
		database = get_reg('database')
		ip = get_reg('ip/host')
		user = get_reg('user')
		password = get_reg('password')

		return backup(database, user, ip, password, tables)
	except:
		print("No values found in registry")


def backup(database, user, ip, password, tables):
	'''Backup to a *.sql file'''

	today = count()
	backup_name = "backup"+today+".sql"

	db = (database[0])
	users = user[0]
	host = ip[0]
	passwd = password[0]
	try:
		for table in tables:
			cmd=[r'mysqldump', '-h', host, '-u', users, '-p%s'%passwd, '%s'%db, table]
			process = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=open(backup_name, 'a'), shell=True)
			process.communicate()
	except:
		print('Mysql operation failed')



# --------------------------------------------------------------------------------------------------
# For linux systems
# --------------------------------------------------------------------------------------------------
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
