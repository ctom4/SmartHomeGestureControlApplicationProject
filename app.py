"""
This Flask application for handling file uploads was primarily developed by the project developer using
The guide "How to Upload File in Python Flask" from GeeksforGeeks which available at:
https://www.geeksforgeeks.org/how-to-upload-file-in-python-flask/. The file was then customized and
modified by the developer to fit the specific needs of this project.
AI assistance, specifically OpenAI's ChatGPT (version GPT-4),
was used to guide the developer when stuck and to clean up and optimize the file.

Attribution:
- OpenAI. "ChatGPT Language Model." Version GPT-4. Accessed September 10, 2024. https://chat.openai.com/.
- GeeksforGeeks. "How to Upload File in Python Flask." https://www.geeksforgeeks.org/how-to-upload-file-in-python-flask/.
"""
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_DIR = './uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


@app.route('/')
def home():
    """
    Home route that provides instructions for file uploading.
    """
    return '''
    <h1>Upload Server</h1>
    <p>POST to /upload to upload files.</p>
    '''


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file uploads. Expects a 'file' field in the request.
    """
    if 'file' not in request.files:
        return error_response("File is missing")

    f = request.files['file']

    if not f.filename:
        return error_response("No file selected")

    # Secure and save the uploaded file
    return save_file(f)


def save_file(f):
    """
    Securely save the uploaded file to the designated upload folder.
    """
    try:
        new_fname = secure_filename(f.filename)
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], new_fname)
        f.save(fpath)
        app.logger.info(f"File saved at: {fpath}")
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error saving file: {str(e)}")
        return jsonify({"error": "Failed to upload file"}), 500


def error_response(message):
    """
    Returns a JSON error response with the provided message.
    """
    app.logger.error(message)
    return jsonify({"error": message}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
