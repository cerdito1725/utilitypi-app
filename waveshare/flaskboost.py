import time
import threading
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def heavy_func():
    time.sleep(20)
    print('Hi!')

@app.route('/', methods=['GET'])
def get_method(): 
    thread = threading.Thread(target=heavy_func)
    thread.daemon = True         # Daemonize 
    thread.start()
    return "work is in progress"
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True),
