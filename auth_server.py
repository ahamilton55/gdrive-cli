#!/usr/bin/env python
"""
This server serves to respond to redirect URL for OAuth2 authentication.

All it does is display the auth code so that you can then take that and
copy paste it into your code.

Author:
    Tom Dignan <tom@tomdignan.com>

Date:
    Wed Apr 25 08:44:42 EDT 2012
"""

from urlparse import parse_qs
import SocketServer
import BaseHTTPServer
import subprocess
from oauth import oauth

PORT = 8081

def run_gdrivefs_startup_script(code):
    pass
"""
    try:
        pidfile = open("gdrivefs.pid", "r")
        pid = pidfile.read()
        pidfile.close()
    except:
        auth_server_process = subprocess.Popen("./fuse/gdrivefs.py")
        pidfile = open("gdrivefs.pid", "w")
        pid = str(auth_server_process.pid)
        pidfile.write(pid)
        pidfile.close()
"""


class AuthRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _get_credentials(authcode):
        return oauth.exchange_code(authcode)

    def _handle_request(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        query = parse_qs(self.path)
        try:
            code = query["code"][0]
        except:
            # Roll over exceptions, the browser requests favicon.ico for example.
            pass

        self.wfile.write("Thank you. Your code is %(code)s Starting GDriveFS..." % { "code" : code 
            })

        print self._get_credentials(code)


if __name__ == '__main__':
    handler = AuthRedirectHandler
    httpd = SocketServer.TCPServer(("", PORT), handler)
    print "Waiting for redirect request at http://localhost:", PORT
    httpd.serve_forever()

