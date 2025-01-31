from flask import Flask,request,jsonify
import util
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="*")

@app.route('/crop_prediction',methods = ['post'])
def classify_crop():  
    data = request.json  
    N = float(data['N'])
    P = float(data['P'])
    K = float(data['K'])	
    temperature = float(data['temp'])
    humidity    = float(data['humid'])
    ph = float(data['ph'])
    rainfall = float(data['rain'])
    
    response = jsonify({
        'estimated':util.classify_crop(N,P,K,temperature,humidity,ph,rainfall)
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response 

if __name__ == '__main__':
    app.run()