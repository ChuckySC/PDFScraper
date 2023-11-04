from flask import Flask, render_template
import datetime

from modules.constants import Constants

app = Flask(__name__)

@app.route('/')
def home():
    # https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
    # return f"{Constants.project_name}: I'm alive. Move on..."
    return render_template('index.html', utc_dt=datetime.datetime.utcnow().date())

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)