from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from bson.json_util import  dumps
from bson.objectid import ObjectId
import datetime
import jwt
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

mongo = PyMongo(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/login')
def login():

    auth = request.authorization

    if auth and auth.username =='user' and  auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])

        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm = "Login Required" '})

if __name__ == '__main__':
    app.run(debug= True)
