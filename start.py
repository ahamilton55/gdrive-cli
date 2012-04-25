#!/usr/bin/env python
"""
Run this to start GDriveFS. Make sure chrome is your default
webbrowser or this will not work.
"""

import webbrowser
import subprocess
from oauth import oauth
import config

pid = None

try:
    pidfile = open("auth_server_process.pid", "r")
    pid = pidfile.read()
    pidfile.close()
except:
    auth_server_process = subprocess.Popen("./auth_server.py")
    pidfile = open("auth_server_process.pid", "w")
    pid = str(auth_server_process.pid)
    pidfile.write(pid)
    pidfile.close()

print "auth server running, pid=", pid
authorize_url = oauth.get_authorization_url(config.email, "local")
webbrowser.open(authorize_url)

