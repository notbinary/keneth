from flask import Flask, current_app, send_from_directory, jsonify
import requests
import json
import os

app = Flask(__name__)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     """ Catch-all route """
#     pass

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def files(path):

    api_token = "testing"
    api_url = "https://fsa-activity-codes.herokuapp.com/"
    headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {api_token}'}

    response = requests.get(api_url, headers=headers)


    if response.status_code == 200:
        return jsonify(json.loads(response.content.decode('utf-8')))
        #return json.loads(response.content.decode('utf-8'))
    else:
        return "That didn't work"

    # p = path if path else 'index.html'
    # return send_from_directory('static', p)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
