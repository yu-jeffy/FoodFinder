from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app._static_folder = 'static'
@app.route('/')

def index():
   return render_template('index.html')




import requests
import json

import googlemaps
from datetime import datetime

apiKey = 'AIzaSyCVIJG9qjcjK59WZ2UIgYpCe7PgEJgL6X8'

gmaps = googlemaps.Client(key=apiKey)









@app.route('/searchFood/', methods=['POST', 'GET'])
def foodFinder():

    input = request.form.to_dict()

    address = input["inputAddress"]

    address.replace(" ", "%20")

    urlCoordinates = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + address + "&inputtype=textquery&fields=formatted_address%2Cgeometry&key=" + apiKey

    payload={}
    headers = {}

    responseCoordinates = requests.request("GET", urlCoordinates, headers=headers, data=payload)


    pythonObjCoordinates = json.loads(responseCoordinates.text)

    print(pythonObjCoordinates)

    lat = pythonObjCoordinates['candidates'][0]['geometry']['location']['lat']
    lng = pythonObjCoordinates['candidates'][0]['geometry']['location']['lng']
    formalAddress = str(pythonObjCoordinates['candidates'][0]['formatted_address'])





    addressLongLat = str(lat) + "%2C" + str(lng)

    urlSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + addressLongLat + "&type=restaurant&radius=8000&opennow=true&key=" + apiKey

    responseSearch = requests.request("GET", urlSearch, headers=headers, data=payload)




    pythonObjSearch= json.loads(responseSearch.text)

    resultsList = dict()

    for item in pythonObjSearch['results']:
        resultsList[item['name']] = [item['vicinity']]




    outputList = []

    for x in resultsList:
        entryTemp = str(x) + "\n" + str(resultsList[x])
        outputList.append(entryTemp)

    outputAddresses = ''.join(outputList)
    outputAddresses = outputAddresses.replace("']", "\n \n ***\n \n")
    outputAddresses = outputAddresses.replace("['", "")
    outputAddresses = outputAddresses.replace("        ", "")


    return render_template('index.html', outputAddresses = outputAddresses, formalAddress = formalAddress)






if __name__ == '__main__':
   app.run(debug=True)
