import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
private_key = os.getenv("GOOGLE_SHEETS_PRIVATE_KEY").replace('\\n', '\n')
private_key_id = os.getenv("GOOGLE_SHEETS_PRIVATE_KEY_ID")
client_id = os.getenv("GOOGLE_SHEETS_CLIENT_ID")
# Define the scope of the API access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

cred = {
  "type": "service_account",
  "project_id": "cs-autotranslation",
  "private_key_id": private_key_id,
  "private_key": private_key,
  "client_email": "523461412539-compute@developer.gserviceaccount.com",
  "client_id": client_id,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/523461412539-compute%40developer.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred, scope)

def update_sheet(email: str, frequency: str, topic: str):
    client = gspread.authorize(creds)
    sheet = client.open("Custom_brew_users").sheet1
    # Add a new row to the sheet
    row = [email, frequency, topic]  # Data to insert
    sheet.append_row(row)
    print(f"User added successfully!: {row}")


def get_all_user_data():
    client = gspread.authorize(creds)
    sheet = client.open("Custom_brew_users").sheet1
    # Get all data from the sheet
    all_rows = sheet.get_all_values()  # List of lists, including header
    data_without_header = [dict(zip(all_rows[0], row)) for row in all_rows[1:]]  # Skip first row and convert to dicts
    return data_without_header

# update_sheet("email@email.com", "Weekly", "News")

# get_all_user_data()