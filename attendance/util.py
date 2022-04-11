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
    "refresh_token": "1//0cz_AXmJs4ukdCgYIARAAGAwSNwF-L9Iruli5JPj2KKFsIFtHTam2BDB4hLlpnyA1nfPsv-9DdbdtSzy5acb1sJcybHuxL_pgx4c",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "82043710113-fvqd9hfbltr2n7hvssag17tbe28emh2u.apps.googleusercontent.com",
    "client_secret": "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",
    "scopes": ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
    "expiry": "2022-04-11T09:16:24.235561Z"}

# gc, authorized_user = gspread.oauth_from_dict(cred2, auth_user)
# print(authorized_user)


class MaintainSpreadSheet:
    def __init__(self):
        # if len(token) == 0:
        #     self.gc, self.authorized_user = gspread.oauth_from_dict(cred2)
        #     teacher = Profile.objects.get(pk=teacher_id)
        #     teacher.auth_token = json.dumps(self.authorized_user)
        #     teacher.save()
        # else:
        #     json_token = json.loads(token)
        self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, auth_user)

    def create_sheet(self, sheet_name):
        self.gc.create(sheet_name)


class WorkWithSpreadSheet:

    def __init__(self, title, work_sheet, user_name, father_name):
        self.user_name = user_name
        self.father_name = father_name
        self.work_sheet = work_sheet

        self.gc, self.authorized_user = gspread.oauth_from_dict(cred2, auth_user)

        self.sheet = self.gc.open(title)

        if not self.is_work_sheet_exist(work_sheet):
            print('helooooo---->', work_sheet)
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
        print(self.work_sheet, '----------------->')
        user_row = self.find_user(self.user_name)
        work_sheet = self.sheet.worksheet(self.work_sheet)
        work_sheet.update_cell(user_row, datetime.now().day + 2, 'present')
        # format_cell_range(work_sheet, f'{datetime.now().day + 2}:{user_row}', header_style)

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
        return False

    @staticmethod
    def set_header(user_name, father_name, work_sheet: str):
        result = list()
        result.append(user_name)
        result.append(father_name)
        for i in range(1, 32):
            result.append(f'{i} {work_sheet[:3]}')
        return result
