import sys, os, ConfigParser
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

# Get authorization link if we don't have access token yet
if not os.path.exists('dropbox.token') or 'force' in sys.argv:

	print '------------------------------------------------'
	print colorize("Creating dropbox session...", 'green')
	sess = session.DropboxSession(dbx_app_key, dbx_app_secret, dbx_access_type)
	
	print colorize("Obtaining request token from dropbox...\n", 'green')
	request_token = sess.obtain_request_token()

	print colorize("Please visit below url in the browser and press the 'Allow' button to authorize this application. After that back here and hit 'Enter'.", 'green')
	print colorize(sess.build_authorize_url(request_token), 'pink')

	print colorize("\nNote: For your convenience url was saved to file named dropbox_authorize_url.", 'yellow')
	print colorize("Do not stop executing this script!", 'red')
	print colorize("You can halt this process (use CTRL+Z) for small piece of time to copy url from terminal and back to them using 'fg' command.", 'yellow')
	
	print colorize("\nPress enter after you authorize this application in browser:", 'green')
	raw_input()

	try:
		print colorize("Obtaining access token from dropbox...", 'green')
		access_token = sess.obtain_access_token(request_token)

		file = open('dropbox.token', 'w+')
		file.write('%s:%s' % (access_token.key, access_token.secret))
		file.close()

		print colorize("Application successfully authorized.", 'green')
	except Exception, e:
		print colorize("Something goes wrong: %s" % e, 'red')
		sys.exit()
else:
	file = open('dropbox.token')
	key, secret = file.read().split(':')
	file.close()

	sess = session.DropboxSession(dbx_app_key, dbx_app_secret, dbx_access_type)
	sess.set_token(key, secret)

	client = client.DropboxClient(sess)

	print colorize("Connected to %s account. Everything is OK!" % client.account_info()['display_name'], 'green')

