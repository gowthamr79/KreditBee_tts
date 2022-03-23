import json
import sched
import time

import gspread
import yaml

from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"
         ]

print("---------------------------sheet schedular server started -----------------------")
with open('config.yml', 'r') as json_data_file:
    json_credentials = yaml.safe_load(json_data_file)
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_credentials, scope)

# authorize the clientsheet
client = gspread.authorize(creds)

# s = sched.scheduler(time.time, time.sleep)


def store_templates_locally(file_name):
    # get the instance of the Spreadsheet
    sheet = client.open('KreditBee responses')
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.worksheet(file_name)
    result1 = sheet_instance.get_all_records(head=1)
    print("-----------------Templates updated locally--------------")
    with open("../{}.json".format(file_name), "w+",  encoding='utf-8') as f:
        json.dump(result1, f, indent=4, ensure_ascii=False)

    # s.enter(900, 1, store_templates_locally, ())


# s.enter(900, 1, store_templates_locally, ())
# s.run()

files_list = ["Sheet1"]
for item in files_list:
    store_templates_locally(item)
