from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
import httplib2
import traceback

"""
Google Drive python module. The code in this file is taken directly from
Google's API reference.

https://developers.google.com/drive/v1/reference/
"""

################################################################################
# Service Object (do this first)                                                                                             #
################################################################################

def build_service(credentials):
    """Build a Drive service object.

    Args:
        credentials: OAuth 2.0 credentials.

    Returns:
        Drive service object.
    """
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('drive', 'v1', http=http)

################################################################################
# Files: get                                                                                                                                     #
################################################################################

def print_file(service, file_id):
    """Print a file's metadata.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to print metadata for.
    """
    try:
        file = service.files().get(id=file_id).execute()

        print 'Title: %s' % file['title']
        print 'Description: %s' % file['description']
        print 'MIME type: %s' % file['mimeType']
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def download_file(service, drive_file):
    """Download a file's content.

    Args:
        service: Drive API service instance.
        drive_file: Drive File instance.

    Returns:
        File's content if successful, None otherwise.
    """
    download_url = drive_file.get('downloadUrl')
    if download_url:
        resp, content = service._http.request(download_url)
        if resp.status == 200:
            print 'Status: %s' % resp
            return content
        else:
            print 'An error occurred: %s' % resp
            return None
    else:
        # The file doesn't have any content stored on Drive.
        return None

################################################################################
# Files: insert                                                                                                                                #
################################################################################

def insert_file(service, title, description, parent_id, mime_type, filename):
    """Insert new file.

    Args:
        service: Drive API service instance.
        title: Title of the file to insert, including the extension.
        description: Description of the file to insert.
        parent_id: Parent folder's ID.
        mime_type: MIME type of the file to insert.
        filename: Filename of the file to insert.
    Returns:
        Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype=mime_type)
    body = {
        'title': title,
        'description': description,
        'mimeType': mime_type
    }

    # Set the parent folder.
    if parent_id:
        body['parentsCollection'] = [{'id': parent_id}]


    try:
        file = service.files().insert(
                body=body,
                media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        # print 'File ID: %s' % file['id']

        return file
    except errors.HttpError, error:
        print "TRACEBACK"
        print traceback.format_exc()
        print 'An error occured: %s' % error
        return None


################################################################################
# Files: patch                                                                                                                                #
################################################################################

def rename_file(service, file_id, new_title):
    """Rename a file.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to rename.
        new_title: New title for the file.
    Returns:
        Updated file metadata if successful, None otherwise.
    """
    try:
        file = {'title': new_title}

        # Rename the file.
        updated_file = service.files().patch(
                id=file_id,
                body=file,
                fields='title').execute()

        return updated_file
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        return None


################################################################################
# Files: update                                                                                                                                #
################################################################################

def update_file(service, file_id, new_title, new_description, new_mime_type,
                                new_filename, new_revision):
    """Update an existing file's metadata and content.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to update.
        new_title: New title for the file.
        new_description: New description for the file.
        new_mime_type: New MIME type for the file.
        new_filename: Filename of the new content to upload.
        new_revision: Whether or not to create a new revision for this file.
    Returns:
        Updated file metadata if successful, None otherwise.
    """
    try:
        # First retrieve the file from the API.
        file = service.files().get(id=file_id).execute()

        # File's new metadata.
        file['title'] = new_title
        file['description'] = new_description
        file['mimeType'] = new_mime_type

        # File's new content.
        media_body = MediaFileUpload(new_filename, mimetype=new_mime_type)

        # Send the request to the API.
        updated_file = service.files().update(
                id=file_id,
                body=file,
                newRevision=new_revision,
                media_body=media_body).execute()
        return updated_file
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        return None
