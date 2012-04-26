import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
import httplib2
import json
import sys

sys.path.append("..")

from db import dbhelper

CLIENTSECRETS_LOCATION = "client_secrets.json"
REDIRECT_URI = "http://localhost:8081"

SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        # Add other requested scopes.
]

class GetCredentialsException(Exception):
    """Error raised when an error occurred while retrieving credentials.

    Attributes:
        authorization_url: Authorization URL to redirect the user to in order to
                                             request offline access.
    """

    def __init__(self, authorization_url):
        """Construct a GetCredentialsException."""
        self.authorization_url = authorization_url


class CodeExchangeException(GetCredentialsException):
    """Error raised when a code exchange has failed."""


class NoRefreshTokenException(GetCredentialsException):
    """Error raised when no refresh token has been found."""


class NoUserIdException(Exception):
    """Error raised when no user ID could be retrieved."""


def get_stored_credentials(user_id):
    """Retrieved stored credentials for the provided user ID.

    Args:
        user_id: User's ID.
    Returns:
        Stored oauth2client.client.OAuth2Credentials if found, None otherwise.
    """

    json_creds = _credentials_row_to_json(dbhelper.get_credentials(user_id))
    creds = json.loads(json_creds)
    print creds
    return OAuth2Credentials.from_json(creds)

def _credentials_row_to_json(row):
    """
    Helper to convert DB row to json. This is yo-yo code and a kludge.

    No time to read the specifics of OAuth2Credentials though, so it will
    be this way for now.
    """

    creds = {
        "_module" : row["_module"],
        "_class" : row["_class"],
        "access_token" : row["access_token"],
        "token_uri" : row["token_uri"],
        "invalid" : row["invalid"],
        "client_id" : row["client_id"],
        "id_token" : {
            "aud" : row["id_token_aud"],
            "cid" : row["id_token_cid"],
            "iss" : row["id_token_iss"],
            "id" : row["id_token_id"],
            "exp" : row["id_token_exp"],
            "iat" : row["id_token_iat"],
            "hash" : row["id_token_token_hash"],
            "email" : row["id_token_email"],
            "verified_email" : row["id_token_verified_email"],
            },
        "client_secret" : row["client_secret"],
        "token_expiry" : row["token_expiry"],
        "refresh_token" : row["refresh_token"],
        "user_agent" : row["user_agent"]
    }

    return json.dumps(creds)

def store_credentials(user_id, credentials):
    """Store OAuth 2.0 credentials in the application's database.

    This function stores the provided OAuth 2.0 credentials using the user ID as
    key.

    Args:
        user_id: User's ID.
        credentials: OAuth 2.0 credentials to store.

    Return:
        Boolean True=Success, False=Failure

    """
    # TODO: Implement this function to work with your database.
    #             To retrieve a Json representation of the credentials instance, call the
    #             credentials.to_json() method.

    dbhelper.create_database_if_nonexistant()
    return dbhelper.insert_or_update_credentials(credentials)

def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
        authorization_code: Authorization code to exchange for OAuth 2.0
                                                credentials.
    Returns:
        oauth2client.client.OAuth2Credentials instance.
    Raises:
        CodeExchangeException: an error occurred.
    """
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    try:
        credentials = flow.step2_exchange(authorization_code)
        return credentials
    except FlowExchangeError, error:
        logging.error('An error occurred: %s', error)
        raise CodeExchangeException(None)


def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information.

    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                                 request.
    Returns:
        User information as a dict.
    """
    user_info_service = build(
            serviceName='oauth2', version='v2',
            http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except errors.HttpError, e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        raise NoUserIdException()


def get_authorization_url(email_address, state):
    """Retrieve the authorization URL.

    Args:
        email_address: User's e-mail address.
        state: State for the authorization URL.
    Returns:
        Authorization URL to redirect the user to.
    """
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'
    flow.params['user_id'] = email_address
    flow.params['state'] = state
    return flow.step1_get_authorize_url(REDIRECT_URI)


def get_credentials(authorization_code, state):
    """Retrieve credentials using the provided authorization code.

    This function exchanges the authorization code for an access token and queries
    the UserInfo API to retrieve the user's e-mail address.
    If a refresh token has been retrieved along with an access token, it is stored
    in the application database using the user's e-mail address as key.
    If no refresh token has been retrieved, the function checks in the application
    database for one and returns it if found or raises a NoRefreshTokenException
    with the authorization URL to redirect the user to.

    Args:
        authorization_code: Authorization code to use to retrieve an access token.
        state: State to set to the authorization URL in case of error.
    Returns:
        oauth2client.client.OAuth2Credentials instance containing an access and
        refresh token.
    Raises:
        CodeExchangeError: Could not exchange the authorization code.
        NoRefreshTokenException: No refresh token could be retrieved from the
                                                         available sources.
    """
    email_address = ''
    try:
        credentials = exchange_code(authorization_code)
        user_info = get_user_info(credentials)
        email_address = user_info.get('email')
        user_id = user_info.get('id')
        if credentials.refresh_token is not None:
            store_credentials(user_id, credentials)
            return credentials
        else:
            credentials = get_stored_credentials(user_id)
            if credentials and credentials.refresh_token is not None:
                return credentials
    except CodeExchangeException, error:
        logging.error('An error occurred during code exchange.')
        # Drive apps should try to retrieve the user and credentials for the current
        # session.
        # If none is available, redirect the user to the authorization URL.
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except NoUserIdException:
        logging.error('No user ID could be retrieved.')
    # No refresh token has been retrieved.
    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)
