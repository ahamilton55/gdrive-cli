#!/usr/bin/env python

from helper import connect

def create_schema():
    conn = connect()
    cursor = conn.cursor()

    """
    tbl_files
        -> tbl_labels
        -> tbl_parentsCollection
        -> tbl_userPermission
    """
    cursor.execute("""
        CREATE TABLE tbl_files (
            createdDate TEXT,
            description TEXT,
            downloadUrl TEXT,
            etag TEXT,
            fileExtension TEXT,
            fileSize TEXT,
            id TEXT PRIMARY KEY,
            kind TEXT,
            lastViewedDate TEXT,
            md5Checksum TEXT,
            mimeType TEXT,
            modifiedByMeDate TEXT,
            modifiedDate TEXT,
            title TEXT
        );
        """)

    """
        tbl_labels
            <- tbl_files
    """
    cursor.execute("""
        CREATE TABLE tbl_labels (
            files_id TEXT,
            hidden INTEGER,
            starred INTEGER,
            trashed INTEGER,
            FOREIGN KEY (files_id) REFERENCES tbl_files(id)
            );
        """)

    """
        tbl_parentsCollection
            <- tbl_files
    """
    cursor.execute("""
        CREATE TABLE tbl_parentsCollection (
            id TEXT,
            files_id TEXT,
            parentLink TEXT,
            FOREIGN KEY (files_id) REFERENCES tbl_files(id)
            );
        """)


    """
        tbl_userPermission
            <- tbl_files
    """
    cursor.execute("""
        CREATE TABLE tbl_userPermission (
            files_id TEXT,
            etag TEXT,
            kind TEXT,
            role TEXT,
            type TEXT,
            FOREIGN KEY (files_id) REFERENCES tbl_files(id)
            );
        """)

    conn.commit()
    cursor.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        print "creating database"
        create_schema()
        print "done"
    else:
        print "usage: ./schema.py create"


