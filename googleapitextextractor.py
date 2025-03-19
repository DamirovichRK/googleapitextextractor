from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
#need to use your own credentials
SERVICE_ACCOUNT_FILE = 'creds.json'
path_to_image = 'testimage.png'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)
media = MediaFileUpload(path_to_image, mimetype='image/png')

file_metadata = {
    'name': 'test4.png',
    'mimeType': 'application/vnd.google-apps.document'
}

res = service.files().create(body=file_metadata, media_body=media).execute()
file_id = res.get('id')

file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

file_id = file.get('id')

# parsing, can skip
resp = service.files().export_media(fileId=file_id, mimeType='text/plain').execute()
contents = resp.decode('utf-8')
contents = ''.join(filter(lambda x: not x.isdigit(), contents))
contents = contents.replace('Вне игры', '')
contents = contents.replace('\r', '')
contents = contents.replace(' ', '\n')
contents = contents.splitlines()
result_list = [x for x in contents if x != '']

# Create a Google Sheets document and send each index of result_list as a row in the table
spreadsheet = {
    'properties': {
        'title': 'ResultList Data'
    }
}

service = build('sheets', 'v4', credentials=creds)
spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
spreadsheet_id = spreadsheet.get('spreadsheetId')

drive_service = build('drive', 'v3', credentials=creds)
mail_creds = 'example@gmail.com'
permissions = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': mail_creds
}

drive_service.permissions().create(fileId=spreadsheet_id, body=permissions).execute()
# Prepare the data as rows
values = [[item] for item in result_list]

# Prepare the request body for inserting data
body = {
    'values': values
}

# Insert data into the first sheet of the spreadsheet
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='Sheet1!A1',
    valueInputOption='RAW',
    body=body
).execute()

print(f"Spreadsheet created with ID: {spreadsheet_id}")
