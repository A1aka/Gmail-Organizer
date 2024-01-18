import os
import pickle
import email
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Your Gmail API scope(s)
# Your Gmail API scope(s)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.modify']


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens and is created
    # automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'YOUR_CREDENTIALS.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def move_email_to_folder(service, user_id, email_id, destination_folder):
    # Create a dictionary to hold the new labels (folders)
    labels = {'removeLabelIds': ['INBOX'],
              'addLabelIds': [destination_folder]}

    # Modify the labels on the specified message to move it to the destination folder
    service.users().messages().modify(userId=user_id,
                                      id=email_id, body=labels).execute()


def organize_emails():
    # Authenticate and create Gmail API service
    credentials = authenticate()
    service = build('gmail', 'v1', credentials=credentials)

    # Set your Gmail address
    user_id = 'me'

    # Set the label (folder) where you want to move emails from a specific sender
    # Replace 'labelId' with the actual label name
    destination_folder = 'labelId'

    # Example: Move emails from 'example@something.comm' to the 'Example' folder
    sender_email = 'example@something.com'

    # Search for emails from the specified sender
    result = service.users().messages().list(
        userId=user_id, q=f'from:{sender_email}').execute()
    messages = result.get('messages', [])

    if not messages:
        print(f"No emails found from {sender_email}")
        return

    print(
        f"Moving {len(messages)} emails from {sender_email} to {destination_folder}...")

    # Move each email to the destination folder
    # Move each email to the destination folder
    # Move each email to the destination folder
    for message in messages:
        email_id = message['id']
        move_email_to_folder(service, user_id, email_id, destination_folder)

    print("Emails moved successfully.")


if __name__ == '__main__':
    organize_emails()
