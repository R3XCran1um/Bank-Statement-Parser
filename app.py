import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from pdf_scanner import master

app = Flask(__name__)

# File upload configurations
UPLOAD_FOLDER = './uploads'
CSV_FOLDER = os.path.abspath('./csv')
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB
# app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)

# Function to check if the uploaded file is allowed (CSV only)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the homepage (file upload form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    # Handling the uploaded CSV file
    if 'csv_file' not in request.files:
        return "No file part"
    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        return "No selected file"
    if csv_file and allowed_file(csv_file.filename):
        csv_filename = secure_filename(csv_file.filename)
        csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        csv_file.save(csv_file_path)
    
    # Handling the selected bank name
    bank_name = request.form.get('bank_name')
    if not bank_name:
        return "No bank selected"
    
    # Handling the optional PDF password
    pdf_password = request.form.get('pdf_password', None)
    
    # Call your custom function to process the CSV file and handle bank-specific logic
    try:
        # Replace this with your actual PDF processing function
        # Assuming your function accepts the CSV path, bank name, and optional PDF password
        master.choose_bank(csv_file_path, bank_name, pdf_password)
        
        # Assuming the function generates a CSV that can be downloaded
        csv_filename = f"{bank_name}_processed.csv"  # You can modify the name as needed
        csv_path = os.path.join(app.config['CSV_FOLDER'], csv_filename)
        
        if os.path.exists(csv_path):
            # Redirect to download the generated CSV file
            return redirect(url_for('download_file', filename=csv_filename))
            return send_file(csv_path, as_attachment=True)

        else:
            return f"CSV file not found at: {csv_path}"
    
    except Exception as e:
        # Handle any errors that occur during the process
        return f"An error occurred: {str(e)}"

# Route to handle file downloads
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['CSV_FOLDER'], filename), as_attachment=True)

# Running the app on the local server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
