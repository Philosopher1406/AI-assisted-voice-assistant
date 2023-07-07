from flask import Flask, render_template
import subprocess

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/jarvis',methods=['POST'])
def jarvis():
    result = subprocess.run(['python', 'jarvis.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout

    try:
        output_text = output.decode('utf-8')
        return output_text
    except UnicodeDecodeError:
        # Handle the case when the output is binary data
        return output



if __name__ == '__main__':
    app.run(debug=True)
