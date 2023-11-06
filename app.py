from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
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

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)