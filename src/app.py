#pip install flask pymongo
#pip install flask-pymongo

from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_URI']='mongodb://192.168.1.49:27017/registros'
PyMongo = PyMongo(app)

@app.route('/user', methods=['POST'])
def create_user():
    return{'msm':'hola'}

if __name__ == "__main__":
    app.run(debug=True)
