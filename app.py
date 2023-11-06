from flask import Flask, render_template, abort, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import os

from functions.universal import allowed_file, load_xml


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'xml'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            'date': datetime.datetime.utcnow().date()
        }
        return render_template('index.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)
        
@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    try:
        file_name = request.args['name']
        file_data = load_xml(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        data = file_data.split('\n')
        return render_template('render_file.html', context={'data': data})
        
        # import xml.etree.ElementTree as ET
        # tree = ET.parse(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        # root = tree.getroot()
        # return render_template('render_file.html', context={'root': root})
        
        # TODO add template that will have one side as xml and on right side a form for adding paramethers for collecting data from xml and structuring them into json
    except Exception as e:
        # logger for errors
        abort(500)  

@app.route('/about')
def about():
    try:
        context = {
            'date': datetime.datetime.utcnow().date()
        }
        return render_template('about.html', context=context)
    except Exception as e:
        # logger for errors
        abort(500)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)