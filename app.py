from flask import Flask, render_template, current_app, send_from_directory, jsonify, redirect, request, abort
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def files():
    return redirect("/static/index.html", code=302)

@app.route('/check', methods = ['POST', 'GET'])
def get_data():

    vrm = request.form.get('vrm')
    if not vrm:
        abort(403)

    reg = vrm[:-3] + " " + vrm[-3:]
    reg = reg.upper()

    dvla = wes_details(vrm)
    dvlasearch = dvlasearch_details(vrm)

    details = {}
    details.update(dvlasearch)
    details.update(dvla)
    standardise_fields(details)
    print(json.dumps(details))

    return render_template('car.html', details=details, reg=reg)

    # p = path if path else 'index.html'
    # return send_from_directory('static', p)

def ves_details(vrm):

    # DVLA API
    api_token = os.getenv('VES_API_KEY', 'DTeXRL3AQn3hTbxKZdiNk4SP6Nih3GRwagMwv3d6')
    if os.getenv('VES_API_KEY'):
        api_url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    else:
        api_url = 'https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_token
        }
    body = {"registrationNumber":vrm}
    print(f'url: {api_url}')
    print(f'key: {api_token}')
    print(f'headers: {headers}')
    print(f'body: {body}')
    response = requests.post(api_url, headers=headers, json=body)
    response_body = response.content.decode('utf-8')
    if response.status_code == 200:
        return json.loads(response_body)
    else:
        print(f"DVLA: That didn't work ({vrm}): {response.status_code}: {response_body}")
        return {}

def dvlasearch_details(vrm):

    # DVLASEARCH API
    api_key = os.getenv('DVLASEARCH_API_KEY', 'ZZyn0nL5TbshFl5J')
    api_url = f'https://dvlasearch.appspot.com/DvlaSearch?apikey={api_key}&licencePlate={vrm}'
    response = requests.get(api_url)
    response_body = response.content.decode('utf-8')
    if response.status_code == 200:
        return json.loads(response_body)
    else:
        print(f"Dvlasearch: That didn't work ({vrm}): {response.status_code}: {response_body}")
        return {}

def standardise_fields(details):

    if details.get('cylinderCapacity'):
        details['engineCapacity'] = details['cylinderCapacity']

    if details.get('taxDetails'):
        details['taxDueDate'] = details['taxDetails'].replace('Tax due: ', '')

    if not details.get('model'):
        details['model'] = ''

# Set up the service account key:
key_data = os.getenv('SERVICE_ACCOUNT_KEY')
with open('key.json', 'w+') as key_file:
    key_file.write(key_data)
wd = os.path.dirname(os.path.realpath(__file__))
key_path = os.path.join(wd, 'key.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
print(f"Key saved to {key_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
