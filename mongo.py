import json
from flask import Flask, jsonify,request, Response
from urllib.request import urlopen
import pymongo
from bson import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient('mongo.servers.nferx.com',username='himanshu.b',password='*')
mydb = client["himanshu"]
mycol1 = mydb["dataset"]  
mycol2 = mydb["models"]  

@app.route('/')
def index():
    return ("Try /project?id to add dataset and models to mongo")

@app.route('/project',methods=["GET"])
def project():
    project_id = request.args.get('id')
    url = "http://sentenceapi2.servers.nferx.com:8015/tagrecorder/v3/projects/" + project_id
    response = urlopen(url)
    data_json = json.loads(response.read())
    mycol1.insert_many(data_json['result']['project']['associated_datasets'])
    mycol2.insert_many(data_json['result']['project']['models'])
    return("Successfully uploaded to mongo")

if __name__=="__main__":
    app.run( host='0.0.0.0', port=81, debug=True)    