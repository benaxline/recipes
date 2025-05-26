from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Setup Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '176rs_PwFxXCOyjtksPWnyLH9LzhVyfvxYYwfLiA5WpQ'
# We'll determine the correct range after getting sheet info

def get_spreadsheet_info():
    """Get detailed information about the spreadsheet"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    
    # Get spreadsheet metadata
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    return spreadsheet

def get_sheet_names():
    """Get all sheet names from the spreadsheet"""
    spreadsheet = get_spreadsheet_info()
    sheet_names = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
    return sheet_names

def get_recipes():
    """Retrieve recipes from Google Sheets"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    
    # Use the correct sheet name with proper formatting
    sheet_name = "Sheet1"  # The exact sheet name from the API
    range_name = f"'{sheet_name}'!A2:E"
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                               range=range_name).execute()
    values = result.get('values', [])
    
    recipes = []
    if values:
        for row in values:
            # Assuming columns: Title, Author, Ingredients, Instructions, Category, Date
            if len(row) >= 5:
                recipe = {
                    'name': row[0],
                    'author': row[1],
                    'type': row[2],
                    'ingredients': row[3].split('\n'),
                    'instructions': row[4].split('\n')
                }
                recipes.append(recipe)
    
    return recipes
