from flask import Flask, render_template, abort, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from functions.universal import allowed_file, load_xml_as_str
from functions.helper import get_structural_data


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['xml']

MAX_ROWS = 3
PARAMETERS = ['font', 'height', 'width', 'line']
BASE = {
    "skip": [],
    "title-start": [],
    "title": [],
    "content-start": [],
    "content": [],
    "author": [],
    "author-start": []
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app.route('/', methods=['GET','POST'])
def index():
    try:
        if request.method == 'POST':
            # Check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']
            # Check if the user selected a file
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
                file_name = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                return redirect(url_for('upload_file', name=file_name))

        context = {
            'date': datetime.utcnow().date()
        }
        return render_template('index.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)
        
@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    try:
        file_name = request.args['name']

        if request.method == 'GET':
            file_data = load_xml_as_str(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            return render_template(
                'render_file.html', 
                context={
                    'type': 'upload',
                    'file_name': file_name,
                    'data': file_data.split('\n'), 
                    'max_rows': MAX_ROWS
                }
            )

        elif request.method == 'POST':
            return render_template(
                'render_file.html', 
                context={
                    'type': 'download',
                    'data': get_structural_data(
                        BASE,
                        PARAMETERS,
                        MAX_ROWS,
                        request.form,
                        os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                    ),
                    'max_rows': MAX_ROWS
                }
            )

        else:
            raise
    except Exception as e:
        # logger for errors
        abort(500)  

@app.route('/about')
def about():
    try:
        context = {
            'date': datetime.utcnow().date()
        }
        return render_template('about.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)