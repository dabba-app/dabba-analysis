import requests
import json
from pprint import pprint
import kmeans as km
import numpy as np
import tsp
import send_asynch_message as sam

# Replace with the correct URL
url = "http://dabba.us-west-2.elasticbeanstalk.com/bins/"

myResponse = requests.get(url)
print (myResponse.status_code)
#print(myResponse.content)

if(myResponse.ok):
    data = json.loads(myResponse.content,encoding="utf-8")
    listOfFilledDustbins = dict()
    listOfFilledDustbins['V1'] = list()
    listOfFilledDustbins['V2'] = list()
    for i in range(len(data)):
        if(data[i]['LEVEL'] > 10):
            listOfFilledDustbins['V1'].append(float(data[i]['LAT']))
            listOfFilledDustbins['V2'].append(float(data[i]['LONG']))

    clusters, C, X = km.kmeans(listOfFilledDustbins)
    for i in range(len(C)):
        points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
        link = tsp.runTsp(points)
        sam.send_message("piyush9620", link + " Follow this route to collect garbage.")
        #print(points)

else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()