from flask import Flask, jsonify, request
# from data_input import data_in  # Assuming data is saved in a separate file
import numpy as np
import json
import pickle

def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

app = Flask(__name__)

# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method == 'GET':
#         # Access data from data_in
#         data = data_in
#         x=data
#         x_in = np.array(x).reshape(1, -1)
#         # print(x_in)
#         # x_in=4.5
#         model = load_models()
#         prediction = model.predict(x_in)[0]
#         print(prediction)
#         response = json.dumps({'response': prediction})
#     elif request.method == 'POST':
#         # Access data from the request body
#         data = request.get_json().get('input')
#     else:
#         return jsonify({'error': 'Method not allowed'})
#
#     # # Perform prediction using the ML model
#     # prediction = "Sample prediction"
#     #
#     # # Prepare response
#     # response = {'result': 'success', 'data': data, 'prediction': prediction}
#
#     # return jsonify(response)
#     return response, 200

@app.route('/predict', methods=['GET','POST'])
def predict():
    # parse input features from request
    request_json = request.get_json()
    x = request_json['input']
    print(x)
    x_in = np.array(x).reshape(1, -1)
    # load model
    model = load_models()
    prediction = model.predict(x_in)[0]
    response = json.dumps({'Estimated Salary in dollar': prediction})
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
