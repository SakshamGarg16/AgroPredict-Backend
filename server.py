from flask import Flask,request,jsonify
import util
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="*")
app.config['SERVER_TIMEOUT'] = 1000

@app.route('/',methods = ['get'])
def index():      
    return "Agro Predict" 

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
        'recommended_crop':util.classify_crop(N,P,K,temperature,humidity,ph,rainfall)
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response 

@app.route('/ferti_prediction',methods = ['post'])
def classify_ferti():  
    data = request.json  
    N = float(data['N'])
    P = float(data['P'])
    K = float(data['K'])	
    temperature = float(data['temp'])
    humidity    = float(data['humid'])
    moist = float(data['moist'])
    soil_type = float(data['soil_type'])
    crop_type = float(data['crop_type'])
    
    response = jsonify({
        'recommended_fertilizer':util.classify_ferti(N,P,K,temperature,humidity,moist,soil_type,crop_type)
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response 

@app.route('/classify_image',methods =["GET","POST"])
def classify_Image():
    image = request.json['image']
    
    response = jsonify({
        "disease_predicted" : util.classify_image(image)})
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response

@app.route('/crop_price',methods = ['post'])
def crop_price():  
    data = request.json  
    State = data['State']
    District = data['District']
    Market = data['Market']	
    Commodity = data['Commodity']
    varity    = data['Varity']
    
    response = jsonify({
        'estimated_price':util.crop_price(State,District,Market,Commodity,varity)
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response 


if __name__ == '__main__':
    app.run(debug=True)
