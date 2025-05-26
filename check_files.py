import os

# Get the absolute path to the frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend'))

# List all files in the frontend directory
print(f"Frontend directory: {frontend_dir}")
print("Files in frontend directory:")
for file in os.listdir(frontend_dir):
    print(f"- {file}")

# Check if recipes.html exists
recipes_path = os.path.join(frontend_dir, 'recipes.html')
if os.path.exists(recipes_path):
    print(f"\nrecipes.html exists at: {recipes_path}")
else:
    print(f"\nrecipes.html DOES NOT exist at: {recipes_path}")