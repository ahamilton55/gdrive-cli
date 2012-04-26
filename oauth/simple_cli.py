import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
from pprint import pprint
from os import getenv

CLIENTSECRETS_LOCATION="client_secrets.json"

SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
]

def authenticate():
    """
    Authenticates and returns OAuth2 credentials.

    Warning, this launches a web browser! You will need to click.
    """
    storage_path = getenv("HOME") + "/.gdrivefs.dat"
    storage = Storage(storage_path)
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    credentials = run(flow, storage)
    return credentials

if __name__ == '__main__':
    authenticate()
