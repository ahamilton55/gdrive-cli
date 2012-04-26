#!/usr/bin/env python
#
# gdrive.py command line google drive client.
#
# Author: Tom Dignan <tom.dignan@gmail.com>
# Date: Thu Apr 26 14:37:20 EDT 2012 
#
# Official Docs: https://developers.google.com/drive/

import argparse
from oauth import simple_cli
from gdrive import gdrive
from os import getenv
from pprint import pprint
import pickle

def _get_pickled_creds_path():
    return getenv("HOME") + "/.gdrive_oauth"

def _get_service_object():
    credentials = _unpickle_credentials()
    return gdrive.build_service(credentials)

def _pickle_credentials():
    credentials = simple_cli.authenticate()
    pickled_creds_path = get_pickled_creds_path()
    pickle.dump(credentials, pickled_creds_path)

def _unpickle_credentials():
    pickled_creds_path = get_pickled_creds_path()
    return pickle.load(pickled_creds_path)

def gdrive_authenticate():
    _pickle_credentials()

def gdrive_print_file(file_id):
    service = _get_service_object()
    gdrive.print_file(service, file_id)

def gdrive_insert():
    print "--insert"

def gdrive_patch():
    print "--patch"

def gdrive_put():
    print "--put"

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="gdrive-cli: google drive interface",
        epilog="Author: Tom Dignan <tom.dignan@gmail.com>")

    parser.add_argument("--print", help="print file metadata", metavar="<file_id>")

    parser.add_argument("--download", help="download file content", metavar="<drive_file>")

    parser.add_argument("--insert", help="insert new file", nargs=5,
            metavar=("<title>", "<description>", "<parent_id>", "<mime_type>", "<filename>"))

    parser.add_argument("--rename", help="rename a file", nargs=2,
            metavar=("<file_id>", "<new_title>"))

    parser.add_argument("--update", help="update file", nargs=6,
            metavar=("<file_id>", "<new_title>", "<new_description>", "<new_mime_type>",
                "<new_filename>", "<new_revision>"))

    args = parser.parse_args()
    pprint(args)


