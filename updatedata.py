from __future__ import print_function
import re
import pickle
import os.path
#from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery as discovery

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#https://docs.google.com/spreadsheets/d/1e4VEZL1xvsALoOIq9V2SQuICeQrT5MtWfBm32ad7i8Q/edit?usp=sharing
SAMPLE_SPREADSHEET_ID = '1e4VEZL1xvsALoOIq9V2SQuICeQrT5MtWfBm32ad7i8Q'
SAMPLE_RANGE_NAME = 'Megyei!A1:U'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokenfile=os.path.expanduser('~/token.pickle')
    if os.path.exists(tokenfile):
        with open(tokenfile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.expanduser('~/credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenfile, 'wb') as token:
            pickle.dump(creds, token)

    service = discovery.build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    values=list(list(int(re.sub('(?<=\d) (?=\d)', '', a)) if re.sub('(?<=\d) (?=\d)', '', a).isdigit() else a for a in row) for row in values)
    

    if not values:
        print('No data found.')
    else:
        for row in values:
            print(*row, sep = "\t")

            
    file = open("datafile.csv","w")
    for row in values:
        txt=""
        for item in range(len(row)):
            txt+=","+str(row[item]) if item > 0 else str(row[item])
        file.write(txt+"\n")
    file.close()

            
if __name__ == '__main__':
    main()

