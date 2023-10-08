from flask import Flask,request,jsonify
import pickle
import numpy as np
from flask_cors import cross_origin
import re

model = pickle.load(open("model_pickle","rb"))

app = Flask(__name__)

@app.route("/predict",methods=["POST"])
@cross_origin(origins=["https://ml-port-scanner.netlify.app"])
def predict():
    test=request.get_json()
    if test is None:
        return jsonify({"error": "Geçersiz istek, veri yok."}), 400
    pattern = r'^[0-9.-]+$'
    data=list(request.get_json().values())
    for value in data:
        if not re.match(pattern,value):
            return jsonify({"error": "Geçersiz istek, hatali veri girisi."}), 400
    np_data=np.array(data)
    prediction=model.predict([np_data])
    if prediction:
        return "Zararlı tarama tespit edildi."
    else:
        return "Zararsız tarama tespit edildi."

if __name__=="__main__":
    app.run(debug=False)