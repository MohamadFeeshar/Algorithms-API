from prediction.data_format import get_data_array
from prediction.neural_network import get_prediction
from flask import Flask, jsonify, request
from os import path
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

site_root = path.realpath(path.dirname(__file__)) + '/'
format_dataset_path = path.join(site_root, 'static/prediction', 'format_dataset.csv')
learning_dataset_path = path.join(site_root, 'static/prediction', 'learning_dataset.csv')


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


if __name__ == '__main__':
    app.run()
