from flask import Flask
import time
import esurv_db_manager as es
app = Flask(__name__, static_folder='./build', static_url_path='/')

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

@app.route('/api/time')
def get_current_time():
    
    return {'time': time.time()}


if __name__ == "__main__":
    app.run(debug=True)


