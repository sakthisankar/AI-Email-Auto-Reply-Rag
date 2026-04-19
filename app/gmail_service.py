import os, base64, pickle, logging
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None

    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'OAuth_credentials_GmailAPI.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def read_emails(service):
    results = service.users().messages().list(
        userId='me', q="is:unread", maxResults=5
    ).execute()

    messages = results.get('messages', [])
    email_data = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id']
        ).execute()

        thread_id = msg_data.get('threadId')
        payload = msg_data['payload']
        headers = payload.get('headers', [])

        sender, subject = "", ""

        for h in headers:
            if h['name'] == 'From':
                sender = h['value']
            if h['name'] == 'Subject':
                subject = h['value']

        data = payload.get('body', {}).get('data', '')
        if not data:
            continue

        text = base64.urlsafe_b64decode(data).decode('utf-8')

        if thread_id:
            email_data.append((msg['id'], thread_id, text, sender, subject))
        else:
            logging.error(f"Missing threadId for {msg['id']}")

    return email_data

def create_draft(service, thread_id, reply, to_email, subject):
    message = MIMEText(reply)
    message['to'] = to_email

    if subject and not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw, 'threadId': thread_id}}
    ).execute()

    logging.info(f"Draft created for {to_email}")
