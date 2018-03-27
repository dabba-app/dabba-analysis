import requests
#from requests.auth import HTTPDigestAuth
import json
from pprint import pprint
import kmeans as km
import numpy as np
import tsp
import send_asynch_message as sam

# Replace with the correct URL
url = "http://dabba.us-west-2.elasticbeanstalk.com/bins/"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)

myResponse = requests.get(url)
print (myResponse.status_code)
#print(myResponse.content)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    data = json.loads(myResponse.content,encoding="utf-8")
    listOfFilledDustbins = dict()
    listOfFilledDustbins['V1'] = list()
    listOfFilledDustbins['V2'] = list()
    for i in range(len(data)):
        #pprint(data[i])
        if(data[i]['LEVEL'] > 10):
            listOfFilledDustbins['V1'].append(float(data[i]['LAT']))
            listOfFilledDustbins['V2'].append(float(data[i]['LONG']))

    #print(listOfFilledDustbins)
    clusters, C, X = km.kmeans(listOfFilledDustbins)
    for i in range(len(C)):
        points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
        link = tsp.runTsp(points)
        sam.send_message("piyush9620", link + " Follow this route to collect garbage.")
        #print(points)


else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()