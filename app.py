from flask import Flask, render_template, current_app, send_from_directory, jsonify, redirect, request, abort
import requests
import json
import tempfile
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import re


app = Flask(__name__)

@app.route('/')
def files():
    return redirect("/static/index.html", code=302)

@app.route('/check', methods = ['POST'])
def get_data():

    vrm = None

    # Try image detection
    if 'photo' in request.files:
        f = request.files['photo']
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            filename = temp.name
        f.save(filename)
        vrm = detect(filename)
        print("Got vrm from photo")
    
    # Fall back to a provided vrm
    if not vrm:
        vrm = request.form.get('vrm')
        print("Falling back to manual vrm")

    # Remove spaces so the APIs understand the vrm:
    vrm = vrm.replace(' ', '')

    dvla = ves_details(vrm)
    dvlasearch = dvlasearch_details(vrm)

    details = {}
    details.update(dvlasearch)
    details.update(dvla)
    standardise_fields(details)
    print(json.dumps(details))

    # User-friendly vrm
    reg = vrm[:-3] + " " + vrm[-3:]
    reg = reg.upper()

    return render_template('car.html', details=details, reg=reg)

    # p = path if path else 'index.html'
    # return send_from_directory('static', p)

def detect(filename):

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(filename)

    # Loads the image into memory
    with open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    print(response)
    labels = response.text_annotations

    print('Labels:')
    for label in labels:
        match = re.search('\\w{2}\\d{2}\\s{0,1}\\w{3}', label.description)
        if match:
            print(f"found: {label.description}")
            vrm = match.group(0)
            print(f"Found vrm: {vrm}")
            return vrm
        else:
            print(f"Not here: {label.description}")

    # Nothing seems to match
    return None
        

def ves_details(vrm):

    # DVLA API
    api_token = os.getenv('VES_API_KEY', 'DTeXRL3AQn3hTbxKZdiNk4SP6Nih3GRwagMwv3d6')
    if os.getenv('VES_API_KEY'):
        api_url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
        print("Using live VES")
    else:
        api_url = 'https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
        print("Using UAT VES")
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_token
        }
    body = {"registrationNumber":vrm}
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



