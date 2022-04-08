from datetime import datetime
from gspread_formatting import *
import gspread
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
import json
from pprint import pprint
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
#
# cred = {
#     "type": "service_account",
#     "project_id": "cool-phalanx-346412",
#     "private_key_id": "725e5f3870ceb16af655ddf0acfeb97d35bba58f",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOHoQASkyE1etk\n4bC/da8Hn8XbQPK2HFB/Dm2/y/EIZDBW8qp3ORwsEzLt3vNGmq6YhZj9uM+b79pF\nvsjCWF69lKAR1M835hnUsCwTWroox7B3RDihGTJ1jmMDHVezZgQyTVRVU8Hz+pHG\nshBHGe0Nq7WrG37iQeTNCjqhwuMNB8qLADnxeghcweioej9uI4CS4j/FGOXAbAJQ\n+zcxcY6PkJo4l8rdEkD7h9ib5/zVxWKLqI9kpXYa27H2V9LMhUmKsTjGelkq0Px8\nq0k0KE7FSt3eysNF3/TJaHXF+Wk6GERNY86NvWj122r9A6PB6D0nX2uwjDx2U+Yb\nd05BWlaTAgMBAAECggEAAi8sspF7QAjjIsb6jx8OScQBi17DI1KUrRp/9s0y4yuc\nXdiN1nUvIv7fp+IM5OwESJQgVa9xUzIA06C0XcvcbHYYBjxbYcfRNKG2dl/DfZa9\nl29g/RCS9wAEWNDx5QMUO/N2Ykgo5qw+oHAy/JaL8GMu7Rd/1V5AkIIJ9iLNQo3W\nrZPKDL7W98mcIzRnLnNKrIy7Tnr5ZUdFxGI8WbeKvOWAoCKlEqEEttWqkO964def\nIM8nzaLgtmANrKjlyHrSuRJhfySYBQ4yC7zjU6nIxq4nCBUxR/nkHpILFTHqK1S4\nOJ+pC8Zg8AcAz3GpcK0KfYqDusBdorFrTcyhS9AdIQKBgQDGO+VInsAPfTmQwmr+\n9iiMLJkjibe7zjTjuU6Z9iILnl53CdV7Ez9yp9k1yZ7ocW1FFUqvVMT8i4mfpoV+\nXIw8cT4oM8oTEShzghLa1AWIuj6ESfdM7q703pGkJH1jcnKeS4r4Avx4g265G/RC\n5LYJ6D8Dv9NVu3CcUvCIkSevXwKBgQC3iIA1wKwAJm+pjGJify7352WTE1cHd6yw\nBNQTZcW87b78SRNL7N+pbVIuh3BvcFJLvapEbk5QH/AWPBP6P4xTKPIEP/YufK+6\nra23eECYhBwuRw3aidGQT4mMu1yhm8z1afyPaL+91TPQlYptovUALGvgtZVfMaiR\n3Fk3b+fJTQKBgBD76r4ZE91/3iG/9ojXsEuqOoin8Pz/QtrL8qcQRoR2UiOizQ6Z\nbJM3PE32c035AeKsW1TAT4xPrD/odYGJDl7TWP76yPJvQub6mwDyr3Kyek69Q5ns\nzUKfmxzUH4YYtSdI06RCJT1yDVeAxKHClLIums+IbOPohlJubLtWrG7DAoGAGBHj\n1qjdJevkixTpNke9zi9fx+kqacVNNYx8j8qyIzP+7zFaQYPgVWUL+SQ0H7lYYayP\nLwhUZve5UgExEYnSCnn9O4dz7ubVWSM7/CreNeJlm8Af1gBrJoT34igUXvGC8NCk\nmd4//1J9yCZEkFplzU8GGuNVorVtiSuf28BmYqUCgYEAvjTUQskS27I1nwTeTV0K\nzJY+0zQ+gAuQk5NIEZfffOmUhp5BauE+UhGKUfxVS/UnAoup1ZzBptq6E4pfsrjg\nf13y1kVTX8TxBhXVHtGQ6NCuwlhvm/RJp0NFg2tknJ3yoeNotVmmAo9UQegS+cro\n437GJQNBZPg70cjj1IVgfsc=\n-----END PRIVATE KEY-----\n",
#     "client_email": "onlineattendance@cool-phalanx-346412.iam.gserviceaccount.com",
#     "client_id": "116600627280021358126",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/onlineattendance%40cool-phalanx-346412.iam.gserviceaccount.com"
# }

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

# fg = {
#     "refresh_token": "1//0cnGF09BHq0jtCgYIARAAGAwSNwF-L9IrUqxqfMR3iMNbMjgmRSB263q980XU8bl72VIWwqJCQ-xSSUA6WY4581h8aoQJfUxBG20",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "client_id": "82043710113-fvqd9hfbltr2n7hvssag17tbe28emh2u.apps.googleusercontent.com",
#     "client_secret": "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",
#     "scopes": ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
#     "expiry": "2022-04-06T17:23:32.548273Z"
# }
fg = {
    "refresh_token": "jsakhdjashdkjasdasd",
    "token_uri": "asdasdasdasdasd",
    "client_id": "asd",
    "client_secret": "",
    "scopes": ["", ""],
    "expiry": "2022-04-06T17:23:32.548273Z"
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


class MaintainSpreadSheet:
    def __init__(self, token: str, teacher_id):
        if len(token) == 0:
            self.gc, self.authorized_user = gspread.oauth_from_dict(cred2)
            teacher = Profile.objects.get(pk=teacher_id)
            teacher.auth_token = json.dumps(self.authorized_user)
            teacher.save()
        else:
            json_token = json.loads(token)
            self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, json_token)

    def create_sheet(self, sheet_name):
        self.gc.create(sheet_name)


class WorkWithSpreadSheet:

    def __init__(self, title, work_sheet, user_name, father_name, token, teacher_id):
        self.user_name = user_name
        self.father_name = father_name
        self.work_sheet = work_sheet

        if not token:
            self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, fg)
            teacher = Profile.objects.get(pk=teacher_id)
            teacher.auth_token = json.dumps(self.authorized_user)
            teacher.save()
        else:
            json_token = json.loads(token)
            self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, json_token)

        try:
            self.sheet = self.gc.open(title)
        except SpreadsheetNotFound:
            self.sheet = self.gc.create(title)

        if not self.is_work_sheet_exist(work_sheet):
            local_work_sheet = self.sheet.add_worksheet(title=work_sheet, rows=100, cols=35)
            local_work_sheet.append_rows(values=[WorkWithSpreadSheet.set_header(
                'Name',
                'Father Name',
                self.work_sheet
            )])
            format_cell_ranges(local_work_sheet, [('1', header_style)])

        if not self.find_user(self.user_name):
            local_work_sheet = self.sheet.worksheet(self.work_sheet)
            local_work_sheet.append_rows(values=[[self.user_name, self.father_name]])

    def take_attendance(self):
        user_row = self.find_user(self.user_name)
        work_sheet = self.sheet.worksheet(self.work_sheet)
        work_sheet.update_cell(user_row, datetime.now().day + 2, 'present')
        # format_cell_range(work_sheet, [('1', header_style)])

    def is_work_sheet_exist(self, work_sheet):
        try:
            self.sheet.worksheet(work_sheet)
            return True
        except WorksheetNotFound:
            return False

    def find_user(self, user_name):
        work_sheet = self.sheet.worksheet(self.work_sheet)
        cell = work_sheet.find(user_name)
        if cell:
            return cell.row
        return None

    @staticmethod
    def set_header(user_name, father_name, work_sheet: str):
        result = list()
        result.append(user_name)
        result.append(father_name)
        for i in range(1, 32):
            result.append(f'{i} {work_sheet[:3]}')
        return result
