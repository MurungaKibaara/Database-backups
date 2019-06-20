import pexpect
import sys

def backup():
	'''Backup to a *.sql file'''

	password = ''
	user = 'root'
	database = ''

	cmd=('mysqldump -u root -p tracking2 -r "backup.sql"')

	child = pexpect.spawn(cmd)
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
