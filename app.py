from flask import Flask, render_template, current_app, send_from_directory, jsonify, redirect, request, abort
import requests
import json
import os

app = Flask(__name__)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     """ Catch-all route """
#     pass

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
@app.route('/')
def files():
    return redirect("/static/index.html", code=302)

@app.route('/check', methods = ['POST', 'GET'])
def get_data():

    vrn = request.form.get('vrn')
    if not vrn:
        abort(403)

    api_token = "DTeXRL3AQn3hTbxKZdiNk4SP6Nih3GRwagMwv3d6"
    api_url = "https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_token
        }
    body = {"registrationNumber":vrn}

    response = requests.post(api_url, headers=headers, json=body)

    response_body = response.content.decode('utf-8')
    if response.status_code == 200:
        print(json.dumps(json.loads(response_body)))
        return render_template('car.html', vrn=vrn)
        #return jsonify(json.loads(response_body))
    else:
        return f"That didn't work ({vrn}): {response.status_code}: {response_body}"

    # p = path if path else 'index.html'
    # return send_from_directory('static', p)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
