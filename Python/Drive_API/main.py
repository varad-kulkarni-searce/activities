from __future__ import print_function

import os.path
import pandas as pd
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']


# To generate the tokens from the credentials file download from GCP
def get_credentials():
    """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/varadkulkarani/Desktop/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


# To access all the files present in the drive
def access_all_files():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # query to get only folders: mimeType = 'application/vnd.google-apps.folder'

        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        # results = service.files().list(fields='1z81EStzOuSmFtRVEhlLpmPDLo_WdBWE1, files(id, name)').execute()
        # items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To access all the files present in the specific folder in list format
def access_specific_folder_files_list():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # query to get only folders: mimeType = 'application/vnd.google-apps.folder'
        folder_id = '1z81EStzOuSmFtRVEhlLpmPDLo_WdBWE1'
        query = f"parents = '{folder_id}'"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To access all the files present in the specific folder in table format (Dataframe)
def access_specific_folder_files_dataframe():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # query to get only folders: mimeType = 'application/vnd.google-apps.folder'
        folder_id = '1z81EStzOuSmFtRVEhlLpmPDLo_WdBWE1'
        query = f"parents = '{folder_id}'"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files')
        pd.set_option('expand_frame_repr', True)
        df = pd.DataFrame(items)
        print(df)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To upload the file from local machine to the drive
def upload_files():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # query to get only folders: mimeType = 'application/vnd.google-apps.folder'
        folder_id = '1z81EStzOuSmFtRVEhlLpmPDLo_WdBWE1'
        # /Users/varadkulkarani/Desktop/Testing

        file_names = ['TestingDocument.docx']
        mime_types = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']

        for file_name, mime_type in zip(file_names, mime_types):
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            media = MediaFileUpload('/Users/varadkulkarani/Desktop/Testing/{0}'.format(file_name),
                                    mimetype=mime_type)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print('File ID: %s' % file.get('id'))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To copy the required file to the specified folder in drive
def copy_files():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # query to get only folders: mimeType = 'application/vnd.google-apps.folder'
        source_file_id = '19loLZUAunAS31X6K82lMPLEaediIURWm'
        folder_ids = ['1z81EStzOuSmFtRVEhlLpmPDLo_WdBWE1']
        # /Users/varadkulkarani/Desktop/Testing
        for folder_id in folder_ids:
            file_metadata = {
                'name': 'TestingDocumentCopy',
                'parents': [folder_id],
                # 'starred': True
            }

            file = service.files().copy(
                body=file_metadata,
                fileId=source_file_id
            ).execute()

            print('File ID: %s' % file.get('id'))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To get all the revisions of a file in google drive
def get_versions():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API

        file_id = '19loLZUAunAS31X6K82lMPLEaediIURWm'
        response = service.revisions().list(
            fileId=file_id,
            fields='*',
            pageSize=1000
        ).execute()

        revisions = response.get('revisions')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = service.revisions().list(
                fileId=file_id,
                fields='*',
                pageSize=1000,
                pageToken=nextPageToken
            ).execute()
            revisions = response.get('revisions')
            nextPageToken = response.get('nextPageToken')
        print(revisions)
        # pd.set_option('expand_frame_repr', True)
        # df = pd.DataFrame(revisions)
        # print(df)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def download_version():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API

        file_id = '19loLZUAunAS31X6K82lMPLEaediIURWm'
        revision_history_id = '0B1KTZEbMS-TwSGVSWm1LTW1JTUxRVW1jRmV2UzJSZUh0aVdFPQ'
        # file_name = 'TestingDocumentDownloaded'
        request = service.revisions().get_media(
            fileId=file_id,
            revisionId=revision_history_id
        )
        with io.FileIO('TestingDocumentPreviousVersion2.docx', 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(status.progress() * 100, '%')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To get all the revisions of a file in google drive
def download_file():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API

        file_id = '19loLZUAunAS31X6K82lMPLEaediIURWm'
        file_name = 'TestingDocumentDownloaded'
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        fh.seek(0)

        with open(os.path.join('/Users/varadkulkarani/Desktop', file_name), 'wb') as f:
            f.write(fh.read())
            f.close()

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    access_all_files()
    access_specific_folder_files_list()
    access_specific_folder_files_dataframe()
    upload_files()
    copy_files()
    get_versions()
    # id_1: 0B1KTZEbMS-TwRTcwcXVCVDJjZUhrcE1sNGVibDdnSkM4eVhRPQ
    # id_2: 0B1KTZEbMS-TwSGVSWm1LTW1JTUxRVW1jRmV2UzJSZUh0aVdFPQ
    download_file()
    download_version()
