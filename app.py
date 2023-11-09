from flask import Flask, render_template, abort, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from functions.universal import allowed_file, load_xml_as_str
from functions.helper import get_structural_data
from modules.configuration import Configuration

configuration = Configuration()


app = Flask(__name__)
app.config['SECRET_KEY'] = configuration.secret_key
app.config['UPLOAD_FOLDER'] = configuration.upload_folder

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

            if file and allowed_file(file.filename, configuration.allowed_extensions):
                file_name = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                return redirect(url_for('upload_file', name=file_name))
            else:
                flash(f'Type of browesed file "{file.filename}" is not allowed.')
                return redirect(request.url)

        # context = {
        #     'date': datetime.utcnow().date()
        # }
        # return render_template('index.html', context=context)
        return render_template('index.html')
    except Exception as e:
        # logger for errors
        abort(500)
        
@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    try:
        file_name = request.args['name']
        file_data = load_xml_as_str(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

        if request.method == 'GET':
            return render_template(
                'render_file.html', 
                context={
                    'data': file_data.split('\n'), 
                    'max_rows': configuration.max_rows
                }
            )

        elif request.method == 'POST':
            return render_template(
                'uploaded_file.html', 
                context={
                    'data': file_data,
                    'structural_data': get_structural_data(
                        configuration.mapping_base,
                        configuration.parameters,
                        configuration.max_rows,
                        request.form,
                        os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                    )
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
        # context = {
        #     'date': datetime.utcnow().date()
        # }
        # return render_template('about.html', context=context)
        return render_template('about.html')
    except Exception as e:
        # logger for errors
        abort(500)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)