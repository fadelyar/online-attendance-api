from datetime import datetime
from gspread_formatting import *
import gspread
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
import json
from user_profile.models import Profile

MONTH_DICTIONARY = {
    '1': 'january',
    '2': 'february',
    '3': 'march',
    '4': 'april',
    '5': 'may',
    '6': 'jun',
    '7': 'july',
    '8': 'august',
    '9': 'september',
    '10': 'october',
    '11': 'november',
    '12': 'december',
}
COLUMNS = {
    '1', 'A',
    '2', 'B',
    '3', 'C',
    '4', 'D',
    '5', 'E',
    '6', 'F',
    '7', 'G',
    '8', 'H',
    '9', 'I',
    '10', 'J',
    '11', 'K',
    '12', 'L',
    '13', 'M',
    '14', 'N',
    '15', 'O',
    '16', 'P',
    '17', 'Q',
    '18', 'R',
    '19', 'S',
    '20', 'T',
    '21', 'U',
    '22', 'W',
    '23', 'X',
    '24', 'Y',
    '25', 'Z',
    '26', 'AA',
    '27', 'AB',
    '28', 'AC',
    '29', 'AD',
    '30', 'AE',
    '31', 'AF',
    '32', 'AG',
    '33', 'AH',
}

cred2 = {
    "installed":
        {"client_id": "82043710113-fvqd9hfbltr2n7hvssag17tbe28emh2u.apps.googleusercontent.com",
         "project_id": "cool-phalanx-346412",
         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
         "token_uri": "https://oauth2.googleapis.com/token",
         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
         "client_secret": "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",
         "redirect_uris": ["http://localhost"]
         }
}

header_style = CellFormat(
    backgroundColor=Color(0, 0, 0),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0.9, 0.9, 0.9)),
    horizontalAlignment='CENTER'
)
present_style = CellFormat(
    backgroundColor=Color(0, 0, 120),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0.9, 0.9, 0.9)),
    horizontalAlignment='CENTER'
)
auth_user = {
    "refresh_token": "1//0ch08ASOv6EIvCgYIARAAGAwSNwF-L9Ir9-TWjwktlfSP9mfj9GGg3YDk6CzHsGeuPv0FairzBMxe4UPtRW4Vg0MktgMrNzyL-K4",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "82043710113-fvqd9hfbltr2n7hvssag17tbe28emh2u.apps.googleusercontent.com",
    "client_secret": "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",
    "scopes": ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
    "expiry": "2022-04-10T19:00:57.047151Z"}


# gc, authorized_user = gspread.oauth_from_dict(cred2, auth_user)


class MaintainSpreadSheet:
    def __init__(self, token: str, teacher_id):
        # if len(token) == 0:
        #     self.gc, self.authorized_user = gspread.oauth_from_dict(cred2)
        #     teacher = Profile.objects.get(pk=teacher_id)
        #     print(self.authorized_user)
        #     teacher.auth_token = json.dumps(self.authorized_user)
        #     teacher.save()
        # else:
        #     json_token = json.loads(token)
        #     self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, json.loads(json_token))

        self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, auth_user)

    def create_sheet(self, sheet_name):
        self.gc.create(sheet_name)


class WorkWithSpreadSheet:

    def __init__(self, sheet, work_sheet, user_name, father_name):
        self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, auth_user)
        self.sheet = sheet
        self.user_name = user_name
        self.father_name = father_name
        self.work_sheet = work_sheet
        self.is_sheet_exist()
        self.is_work_sheet_exist()

    def is_work_sheet_exist(self):
        try:
            sh = self.gc.open(self.sheet)
            wk = sh.worksheet(self.work_sheet)
        except WorksheetNotFound:
            sh = self.gc.open(self.sheet)
            sh.add_worksheet(self.work_sheet)

    def is_sheet_exist(self):
        try:
            self.gc.open(self.sheet)
        except SpreadsheetNotFound:
            self.gc.create(self.sheet)
