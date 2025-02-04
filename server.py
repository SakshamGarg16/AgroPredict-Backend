from flask import Flask,request,jsonify
import util
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
CORS(app, origins="*")

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 40
    image = request.files['image']
    
    
    try:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        predicted_label = util.classify_image(path=image_path)

        os.remove(image_path)

        return jsonify({"disease_predicted": predicted_label})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
