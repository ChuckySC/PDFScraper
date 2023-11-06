from flask import (
    Flask, 
    render_template, 
    send_from_directory
)
import datetime
import os

from modules.constants import Constants

app = Flask(__name__)

@app.route('/')
def index():
    # return f"{Constants.project_name}: I'm alive. Move on..."
    context = {
        'date': datetime.datetime.utcnow().date()
    }
    return render_template('index.html', context=context)

@app.route('/about')
def about():
    context = {
        'date': datetime.datetime.utcnow().date()
    }
    return render_template('about.html', context=context)


# TODO resolve GET /static/favicon.ico HTTP/1.1" 404
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)