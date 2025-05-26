from flask import Flask, send_from_directory
import os

# Create a simple Flask app
app = Flask(__name__)

# Get the absolute path to the frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend'))
print(f"Frontend directory: {frontend_dir}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    print(f"Requested path: {path}")
    
    if not path:
        # Serve index.html for root path
        return send_from_directory(frontend_dir, 'index.html')
    
    file_path = os.path.join(frontend_dir, path)
    print(f"Looking for: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Get the directory and filename
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        print(f"Serving {filename} from {directory}")
        return send_from_directory(directory, filename)
    else:
        # Fallback to index.html
        print("Fallback to index.html")
        return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    # List all files in the frontend directory
    print("Files in frontend directory:")
    try:
        for file in os.listdir(frontend_dir):
            print(f"- {file}")
    except Exception as e:
        print(f"Error listing files: {e}")
    
    app.run(debug=True, port=5001)