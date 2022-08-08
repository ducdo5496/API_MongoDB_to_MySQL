from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from bson.json_util import  dumps
from bson.objectid import ObjectId
import jwt
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

app.config['MONGO_URI']="mongodb://10.86.94.2:27017/team2db"
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

#Fetch toàn bộ dữ liệu từ collection company:
@app.route('/api/company',methods=['GET'])
@token_required
def data_company():
    if request.method == 'GET':
        data=mongo.db.company.find()
        resp=dumps(data)
        return resp
    return -1

#Fetch data từ id;
@app.route('/api/company/<id>',methods = ['GET'])
@token_required
def conpany(id):
    if request.method == 'GET':
        conpany=mongo.db.company.find_one({'_id': ObjectId(id)})
        resp=dumps(conpany)
        return resp
    return -1

# @app.route('/recruitments')
# @token_required
# def data_recruitments():
#     data = mongo.db.recruitments.find()
#     resp=dumps(data)
#     return resp
#
# @app.route('/recruitments/<id>')
# @token_required
# def recruitments(id):
#     recruitments=mongo.db.recruitments.find_one({'_id': ObjectId(id)})
#     resp=dumps(recruitments)
#     return resp

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'Not found'+request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(host='10.86.94.1')
