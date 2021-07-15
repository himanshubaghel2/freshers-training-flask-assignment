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
    return ("Try /project?id or /model?id or /dataset?id")

@app.route('/project',methods=["GET"])
def project():
    project_id = request.args.get('id')
    url = "http://sentenceapi2.servers.nferx.com:8015/tagrecorder/v3/projects/" + project_id
    response = urlopen(url)
    data_json = json.loads(response.read())
    return(jsonify(data_json))

@app.route('/dataset',methods=["GET"])
def dataset():
    dataset_id = request.args.get('id')
    myquery = {"_id": dataset_id}
    mydoc = mycol1.find(myquery)
    list_cur = list(mydoc)
    jss=json.dumps(list_cur)
    js=json.loads(jss)
    return (jsonify(js))

@app.route('/models',methods=["GET"])
def model():
    model_id = request.args.get('id')
    myquery = {'_id':ObjectId(model_id)}
    mydoc = mycol2.find(myquery)
    list_cur = list(mydoc)
    jss=json.dumps(list_cur , default=str)
    js=json.loads(jss)
    return(jsonify(js))

if __name__=="__main__":
    app.run(debug=True)