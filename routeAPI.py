from flask import Flask, request
from flask_cors import CORS, cross_origin
import joblib
import numpy as np
 
app = Flask(__name__)
CORS(app)
 
@app.route('/')
def helloworld():
    return 'Helloworld'
 
@app.route('/area', methods=['GET'])
@cross_origin()
def area():
    w = float(request.values['w'])
    h = float(request.values['h'])
    return str(w * h)
 
@app.route('/bmi', methods=['GET'])
@cross_origin()
def bmi():
    weight = float(request.values['weight'])
    height = float(request.values['height'])
    return str(weight / ((height/100) * (height/100)))
 
@app.route('/iris', methods=['POST'])
@cross_origin()
def predict_species():
    model = joblib.load('iris.model')
    req = request.values['param']
    inputs = np.array(req.split(','), dtype=np.float32).reshape(1,-1)
    predict_target = model.predict(inputs)
    if predict_species == 0:
        return 'Setosa'
    elif predict_species == 1:
        return 'Versicolour'
    else:
        return 'Virginica'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
