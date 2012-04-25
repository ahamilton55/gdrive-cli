from apiclient import errors
# ...

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
    if error.resp.status == 401:
      # Credentials have been revoked.
      # TODO: Redirect the user to the authorization URL.
      raise NotImplementedError()
