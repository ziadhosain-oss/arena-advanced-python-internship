from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload form template
upload_form = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload a File</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)
            return f'File uploaded successfully! <a href="/files/{uploaded_file.filename}">Click here to view/download</a>'
        return 'No file selected'
    return render_template_string(upload_form)

@app.route('/files/<filename>')
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)