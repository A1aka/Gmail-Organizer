import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Your Gmail API scope(s)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels']


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
                'YOUR_CREDENTIALS_FILE.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def list_labels(service, user_id):
    results = service.users().labels().list(userId=user_id).execute()
    labels = results.get('labels', [])
    return labels


if __name__ == '__main__':
    credentials = authenticate()
    service = build('gmail', 'v1', credentials=credentials)
    user_id = 'me'

    labels = list_labels(service, user_id)

    for label in labels:
        print(f"Label Name: {label['name']}, Label ID: {label['id']}")
