from backend.utils.sheets import get_recipes, get_sheet_names, get_spreadsheet_info
import json

# Print detailed spreadsheet info
try:
    print("Spreadsheet information:")
    spreadsheet_info = get_spreadsheet_info()
    # Print just the sheet names and IDs for clarity
    print("Sheets in this spreadsheet:")
    for sheet in spreadsheet_info['sheets']:
        props = sheet['properties']
        print(f"- Sheet ID: {props['sheetId']}, Title: '{props['title']}'")
except Exception as e:
    print(f"Error getting spreadsheet info: {e}")

# Then try to get recipes
try:
    recipes = get_recipes()
    print(f"\nSuccessfully retrieved {len(recipes)} recipes:")
    for i, recipe in enumerate(recipes[:3], 1):  # Print first 3 recipes
        print(f"{i}. {recipe['name']} by {recipe['author']}")
except Exception as e:
    print(f"\nError getting recipes: {e}")
