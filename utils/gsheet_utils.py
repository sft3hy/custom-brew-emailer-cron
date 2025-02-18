import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
cred = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS"))
# Define the scope of the API access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account's JSON file
# creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/service-account-file.json', scope)
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred, scope)

def update_sheet(email: str, frequency: str, topic: str):
    client = gspread.authorize(creds)
    sheet = client.open("Custom_brew_users").sheet1
    # Add a new row to the sheet
    row = [email, frequency, topic]  # Data to insert
    sheet.append_row(row)
    print(f"Row added successfully!: {row}")


def get_all_user_data():
    client = gspread.authorize(creds)
    sheet = client.open("Custom_brew_users").sheet1
    # Get all data from the sheet
    all_rows = sheet.get_all_values()  # List of lists, including header
    data_without_header = [dict(zip(all_rows[0], row)) for row in all_rows[1:]]  # Skip first row and convert to dicts

    # print(data_without_header)
    return data_without_header

# update_sheet("email@email.com", "Weekly", "News")

# get_all_user_data()