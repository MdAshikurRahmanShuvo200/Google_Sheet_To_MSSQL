import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetReader:

    def __init__(self, sheet_id, credential_file):

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        creds = Credentials.from_service_account_file(
            credential_file,
            scopes=scopes
        )

        client = gspread.authorize(creds)

        self.workbook = client.open_by_key(sheet_id)

    def get_all_worksheets(self):
        return self.workbook.worksheets()

    def get_sheet_data(self, worksheet):

        return worksheet.get_all_values()