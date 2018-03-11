from prediction.data_format import get_data_array
from prediction.neural_network import get_prediction
from recommendation.recommend import recommend
from recommendation.data_format_rec import data_list
from flask import Flask, jsonify, request
from os import path
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

site_root = path.realpath(path.dirname(__file__)) + '/'
format_dataset_path = path.join(site_root, 'static/prediction', 'format_dataset.csv')
learning_dataset_path = path.join(site_root, 'static/prediction', 'learning_dataset.csv')
dataset_path = path.dirname(path.abspath(__file__))+'/static/recommendation/Dataset-Original.csv' 

@app.route('/prediction', methods=['POST'])
def prediction():

    user = request.get_json()

    if not user:
        return 'Not A Valid Json Request'

    result = get_prediction(get_data_array(user, format_dataset_path), learning_dataset_path)

    courses = {
        'courses': []
    }

    for i in range(len(user['courses'])):
        course = {
            'id': user['courses'][i]['id'],
            'prediction': float(format(result[i], '.2f'))
        }
        courses['courses'].append(course)

    return jsonify(courses)

@app.route('/recommendation', methods=['POST'])
def recommendation():
    json_data = request.get_json()
    if not json_data:
        return 'Not A Valid Json Request'
    data = data_list(json_data)
    
    
    result, student = [], []
    student = data[0]
    result.append(recommend(dataset_path, student))
    for i in range(1,len(data)):
        student = data[i]
        result.append(recommend(dataset_path, student))
    

    courses = {
        'general_recommendation':[],
        'courses': [],
    }
    general_recommendation = {}

    if 'traveltime' in result[0]:
        general_recommendation['decrease travel time by '] = result[0]['traveltime']    
    if 'freetime' in result[0]:
        general_recommendation['increase free time by '] = result[0]['freetime']

    if 'goout' in result[0]:
        general_recommendation['increase go out by'] = result[0]['goout']
    courses['general_recommendation'].append(general_recommendation)
    
    for i in range(len(json_data['courses'])):
        
        course = {
            'id': json_data['courses'][i]['id']
        }

        if 'studytime' in result[i]:
            course['increase study time by'] = result[i]['studytime']
        
        if 'absences' in result[i]:
            course['decrease absences by'] = result[i]['absences']

        courses['courses'].append(course)
    return jsonify(courses)
     


if __name__ == '__main__':
    app.run()
