from flask import Flask, render_template

from modules.constants import Constants

app = Flask(__name__)

@app.route('/')
def home():
    #return f"{Constants.project_name}: I'm alive. Move on..."
    return render_template('index.html')

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)