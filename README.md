WORK IN PROGRESS. PLEASE COME BACK IN A FEW HOURS. NOT DONE YET.

I was too impatient to wait for google to release their Linux version of Google 
Drive, so I made one with FUSE.

How to use:

Run start.py. It will open a tab in chrome to authenticate you with oauth, and then
spawn a local webserver. The webserver will capture your authentication code and use
it to start gdrivefs. GDriveFS will be mounted on ~/GDriveFS.

Dependencies:

sudo pip install google-api-python-client



