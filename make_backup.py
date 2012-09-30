#!/usr/bin/python

import os, time, ConfigParser, sys
from dropbox import client, rest, session
from colorize import colorize

config = ConfigParser.ConfigParser()
config.read('config.ini')

# Get configuration first
try:
	db_user = config.get('Database', 'user')
	db_password = config.get('Database', 'password')
	db_host = config.get('Database', 'host')
	dbx_app_key = config.get('Dropbox', 'app_key')
	dbx_app_secret = config.get('Dropbox', 'app_secret')
	dbx_access_type = config.get('Dropbox', 'access_type')
except ConfigParser.NoOptionError, e:
	print colorize('Configuration file error. %s' % e, 'red')
	sys.exit()

# Temporary directory to which database dumps will be saved
# before they will be uploaded to dropbox account.
output_dir = ur'output/'

# Create backup directory if not exists
if not os.path.exists(output_dir):
	os.makedirs(output_dir)

command = "mysql -u %s -p%s -h %s --silent -N -e 'show databases'" % (db_user, db_password, db_host)
today = time.strftime('%Y-%m-%d')

print '------------------------------------------------'

for database in os.popen(command).readlines():
	database = database.strip()

	if database == 'information_schema':
		continue

	sys.stdout.write(colorize("Dumping", 'green') + colorize(' %s' % database, 'pink') + colorize(' -> ', 'green'))
	filename = output_dir + '%s-%s.sql' % (database, today)
	os.popen('mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz' % (db_user, db_password, db_host, database, filename))
	print colorize("Done", 'green')

print colorize("Connecting to dropbox...", 'green')

file = open('dropbox.token')
key, secret = file.read().split(':')
file.close()

# Create name for this server. Name contains server hostname and current user name.
server_name = '-'.join( [v.strip() for v in os.popen('hostname && whoami').readlines()] ).strip()

try:
	sess = session.DropboxSession(dbx_app_key, dbx_app_secret, dbx_access_type)
	sess.set_token(key, secret)

	client = client.DropboxClient(sess)

	for dirpath, dirs, files in os.walk(output_dir):
		for file in files:
			fullpath = dirpath + file
			f = open(fullpath)
			sys.stdout.write( colorize("Uploading file ", 'green') + colorize(file, 'pink') + colorize(' -> ', 'green') )
			response = client.put_file('/'+server_name+'/'+today+'/'+file, f)
			print colorize("Uploaded.", 'green')

			os.remove(fullpath)

except Exception, e:
	print colorize("Something goes wrong: %s" % e, 'red')
	sys.exit()