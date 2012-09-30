# Glaw

Glaw is a simply python script which will dumps all Mysql databases and upload them to Dropbox.

# Installation

1. Install Dropbox python SDK. Go there https://www.dropbox.com/developers/start/setup#python and follow the steps - it takes only few minutes.
2. Create your Dropbox App here https://www.dropbox.com/developers/apps (named it what you like).
2. Upload script to your server (location does not matter).
3. Rename `example.config.ini` to `config.ini` and edit it.
4. Run `authoize_dropbox_app.py` to authorize access of application to your Dropbox account (type this to command line `python authorize_dropbox_app.py`)
5. Installation done!

Now you can execute `make_backup.py` to dumps all databases and upload them to your Dropbox account.

	$ python make_backup.py

Warning: I do not take any responsibility if due to the use of this script, your world will explode! You are using this on your own risk :)