from __future__ import print_function

import os.path
import pandas as pd
import io
from fastapi import FastAPI
import uvicorn
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

app = FastAPI()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


# To generate the tokens from the credentials file download from GCP
def get_credentials(credentials_path):
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
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


# To access all the files present in the drive
@app.api_route('/access_all_files', methods=["GET"])
def access_all_files(credentials_path):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=20, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files')
        if not items:
            print('No files found.')
            return
        return items

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To access all the files present in the specific folder in list format
@app.api_route("/access_specific_folder_in_list_format", methods=["GET"])
def access_specific_folder_files_list(credentials_path, folder_id):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        query = f"parents = '{folder_id}'"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files')
        if not items:
            print('No files found.')
            return
        return items

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To access all the files present in the specific folder in table format (Dataframe)
@app.api_route("/access_specific_folder_in_dataframe_format", methods=["GET"])
def access_specific_folder_files_dataframe(credentials_path, folder_id):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        query = f"parents = '{folder_id}'"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files')
        pd.set_option('expand_frame_repr', True)
        df = pd.DataFrame(items)
        return df

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To upload the file from local machine to the drive
@app.api_route("/upload_files", methods=["POST"])
def upload_files(credentials_path, folder_id, file_name, mime_type, file_path):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': file_name,
            'parents': folder_id
        }
        media = MediaFileUpload(file_path.format(file_name),
                                mimetype=mime_type)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To copy the required file to the specified folder in drive
@app.api_route("/make_clone", methods=["POST"])
def copy_files(credentials_path, source_file_id, folder_id, file_name):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': file_name,
            'parents': folder_id,
        }
        file = service.files().copy(
            body=file_metadata,
            fileId=source_file_id
        ).execute()
        return file.get('id')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# Function to clone specific version of a file..
# steps: download_version -> upload_version -> copy_version
@app.api_route("/copy_version", methods=["POST"])
def copy_version(credentials_path, file_id, revision_history_id, revision_file_name, folder_id, mime_type):
    download_version(credentials_path, file_id, revision_history_id, revision_file_name)
    file_path = revision_file_name
    source_file_id = upload_files(credentials_path, folder_id, revision_file_name, mime_type, file_path)
    file_name = revision_file_name + '_copy'
    copy_file_id = copy_files(credentials_path, source_file_id, folder_id, file_name)
    return copy_file_id


# To get all the revisions of a file in google drive
@app.api_route("/get_versions", methods=["GET"])
def get_versions(credentials_path, file_id):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
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
            nextsPageToken = response.get('nextPageToken')
        return revisions

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


@app.api_route("/download_versions", methods=["GET"])
def download_version(credentials_path, file_id, revision_history_id, revision_file_name):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        request = service.revisions().get_media(
            fileId=file_id,
            revisionId=revision_history_id
        )
        with io.FileIO(revision_file_name, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(status.progress() * 100, '%')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# To get all the revisions of a file in google drive
@app.api_route("/download_file", methods=["GET"])
def download_file(credentials_path, file_id, file_name, download_path):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)
        with open(os.path.join(download_path, file_name), 'wb') as f:
            f.write(fh.read())
            f.close()

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


@app.api_route('/permissions', methods=["POST"])
def permissions(credentials_path, file_id, user_email, user_role, user_type):
    creds = get_credentials(credentials_path)
    try:
        service = build('drive', 'v3', credentials=creds)
        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            'type': user_type,
            'role': user_role,
            'emailAddress': user_email
        }
        batch.add(service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ))
        batch.execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


@app.api_route("/send_email_without_attachment", methods=["POST"])
def send_email_without_attachment(sender_email, sender_password, receiver_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)         # creates SMTP session
    s.starttls()        # start TLS for security
    s.login(sender_email, sender_password)          # Authentication
    message = "Message_you_need_to_send"                            # message to be sent
    s.sendmail(sender_email, receiver_email, message)     # sending the mail
    s.quit()


@app.api_route('/send_email_with_subject_and_attachment', methods=["POST"])
def send_email_with_subject_and_attachment(sender_email, sender_password, receiver_email, email_subject, email_body, attachment_file_with_extension, file_path):

    fromaddr = sender_email
    toaddr = receiver_email

    msg = MIMEMultipart()                # instance of MIMEMultipart
    msg['From'] = fromaddr
    msg['To'] = toaddr                      # storing the receivers email address

    msg['Subject'] = email_subject          # storing the subject
    body = email_body                       # string to store the body of the mail
    msg.attach(MIMEText(body, 'plain'))         # attach the body with the msg instance

    filename = attachment_file_with_extension       # open the file to be sent
    attachment = open(file_path, "rb")

    p = MIMEBase('application', 'octet-stream')     # instance of MIMEBase and named as p
    p.set_payload((attachment).read())              # To change the payload into encoded form
    encoders.encode_base64(p)                        # encode into base64
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)                               # attach the instance 'p' to instance 'msg'

    s = smtplib.SMTP('smtp.gmail.com', 587)             # creates SMTP session
    s.starttls()                                    # start TLS for security
    s.login(fromaddr, sender_password)              # Authentication
    text = msg.as_string()                          # Converts the Multipart msg into a string
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
