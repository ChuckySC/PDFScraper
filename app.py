from flask import Flask, render_template, abort, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os

from functions.universal import allowed_file, load_xml_as_str, save_json
from functions.helper import get_structural_data
from modules.configuration import Configuration

configuration = Configuration()


app = Flask(__name__)
app.config['SECRET_KEY'] = configuration.secret_key
app.config['UPLOAD_FOLDER'] = configuration.upload_folder

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

@app.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app.route('/', methods=['GET','POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # logger for errors
        abort(500)

@app.route('/about', methods=['GET'])
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        # logger for errors
        abort(500)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url_root)

        file = request.files['file']
        # Check if the user selected a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url_root)

        if file and allowed_file(file.filename, configuration.allowed_extensions):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            return redirect(url_for('render_file', name=file_name))
        else:
            flash(f'Type of browesed file "{file.filename}" is not allowed.')
            return redirect(request.url_root)

    except Exception as e:
        # logger for errors
        abort(500)

@app.route('/render_file', methods=['GET','POST'])
def render_file():
    try:
        file_name = secure_filename(request.args['name'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file_data = load_xml_as_str(file_path)

        if request.method == 'GET':
            return render_template(
                'render_file.html', 
                context={
                    'data': file_data.split('\n'), 
                    'max_rows': configuration.max_rows
                }
            )

        elif request.method == 'POST':
            structural_data = get_structural_data(
                configuration.mapping_base,
                configuration.parameters,
                configuration.max_rows,
                request.form,
                file_path
            )

            save_json(
                data = structural_data,
                file_name=file_path.replace('.xml', '.json')
            )
            
            return render_template(
                'download_file.html', 
                context={
                    'file_name': file_name,
                    'data': file_data,
                    'structural_data': structural_data
                }
            )

        else:
            raise

    except Exception as e:
        # logger for errors
        abort(500)

@app.route('/download/<file_name>/<type>', methods=['GET','POST'])
def download(file_name, type):
    try:
        name_json = str(file_name).replace('.xml', '.json')
        path_json = os.path.join(app.config['UPLOAD_FOLDER'], name_json)
        
        if type == 'json':
            return send_from_directory(
                directory=app.config['UPLOAD_FOLDER'], 
                path=name_json,
                as_attachment=True
            )

        elif type == 'csv':
            name_csv = str(file_name).replace('.xml', '.csv')
            path_csv = os.path.join(app.config['UPLOAD_FOLDER'], name_csv)

            pd.read_json(path_json).to_csv(path_csv)

            return send_from_directory(
                directory=app.config['UPLOAD_FOLDER'], 
                path=name_csv,
                as_attachment=True
            )

        elif type == 'excel':
            name_xlsx = str(file_name).replace('.xml', '.xlsx')
            path_xlsx = os.path.join(app.config['UPLOAD_FOLDER'], name_xlsx)

            pd.read_json(path_json).to_excel(path_xlsx)

            return send_from_directory(
                directory=app.config['UPLOAD_FOLDER'], 
                path=name_xlsx,
                as_attachment=True
            )

        else:
            raise
    except Exception as e:
        # logger for errors
        abort(500)