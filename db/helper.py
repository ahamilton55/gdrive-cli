"""
Helper methods for database
"""

import sqlite3
import os

def connect():
    dbpath = os.getenv("HOME") + os.path.sep + ".gdrive-cli.db"
    return sqlite3.connect(dbpath)


"""
Inserts file metadata returned by gdrive.insert_file into the
tbl_files table and tables related to it.

Returns:
    id of the inserted data
"""
def insert_file(metadata):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_files (
            createdDate,
            description,
            downloadUrl,
            etag,
            fileExtension,
            fileSize,
            id,
            kind,
            lastViewedDate,
            md5Checksum,
            mimeType,
            modifiedByMeDate,
            modifiedDate,
            title
        ) VALUES (
           ?,?,?,?,?,?,?,?,?,?,?,?,?,?
        );
        """, (
            metadata["createdDate"],
            metadata["description"],
            metadata["downloadUrl"],
            metadata["etag"],
            metadata["fileExtension"],
            metadata["fileSize"],
            metadata["id"],
            metadata["kind"],
            metadata["lastViewedDate"],
            metadata["md5Checksum"],
            metadata["mimeType"],
            metadata["modifiedByMeDate"],
            metadata["modifiedDate"],
            metadata["title"],
            )
        );

    cursor.execute("""
        INSERT INTO tbl_labels (
            files_id,
            hidden,
            starred,
            trashed
        ) VALUES (
            ?,?,?,?
        );
        """, (
            metadata["id"],
            metadata["labels"]["hidden"],
            metadata["labels"]["starred"],
            metadata["labels"]["trashed"],
        )
    );

    for parent in metadata["parentsCollection"]:
        cursor.execute("""
            INSERT INTO tbl_parentsCollection (
                id,
                files_id,
                parentLink
            ) VALUES (
                ?,?,?
            );
            """, (
                parent["id"],
                metadata["id"],
                parent["parentLink"],
            )
        );

    cursor.execute("""
        INSERT INTO tbl_userPermission (
            files_id,
            etag,
            kind,
            role,
            type
        ) VALUES (
            ?,?,?,?,?
        )
        """, (
            metadata["id"],
            metadata["userPermission"]["etag"],
            metadata["userPermission"]["kind"],
            metadata["userPermission"]["role"],
            metadata["userPermission"]["type"],
        )
    );


    conn.commit()
    cursor.close()

    return metadata["id"]

def select_all_files():
    """
    Generates a basic listing of files in tbl_files
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT title, id FROM tbl_files")
    files = cursor.fetchall()
    cursor.close()
    conn.commit()

    return files






