from flask import Flask, render_template, abort
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    try:
        context = {
            'date': datetime.datetime.utcnow().date()
        }
        return render_template('index.html', context=context)
    except Exception as e:
        # logger for errors
        abort(404)
        
@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('create.html')
    

@app.route('/about')
def about():
    try:
        context = {
            'date': datetime.datetime.utcnow().date()
        }
        return render_template('about.html', context=context)
    except Exception as e:
        # logger for errors
        abort(404)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)