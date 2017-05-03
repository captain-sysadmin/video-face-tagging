#coding=utf-8
import os
import sys
import json
import requests

try:
    capiKey = os.environ['CAPI_KEY']
    msKey   = os.environ['MS_KEY']
except:
    print "please set the env-var CAPI_KEY with a valid key"
    sys.exit(3)
r = requests.get('http://api.ft.com/sixdegrees/mostMentionedPeople?fromDate=2017-03-07&limit=100&apiKey={0}'.format(capiKey))
if r.status_code == requests.codes.ok:
    names = r.json()
else:
    print "got a {0} error trying to talk to capi".format(r.status_code)
    

print names[0]
for name in names:
    idUrl = name['id']
    name = name['prefLabel']
    nameParts = name.split(' ')
    shortName = u"{0} {1}".format(nameParts[0], nameParts[-1])
    #print idUrl+'&apiKey={0}'.format(capiKey)
    print shortName
    asciiName = unicode(shortName).encode('ascii', 'replace')
    search = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={0}&count=5&mrkt=en-GB'.format(asciiName), headers= {'Ocp-Apim-Subscription-Key': msKey})
    print search.status_code
    for count, image in enumerate(search.json()['value']):
        try:
            imageReq = requests.get(image['contentUrl'], stream=True)
            with open("candidates/{0}-{1}.jpg".format(asciiName.replace(' ', '-'),count), 'wb') as imageFile:
                for chunk in imageReq.iter_content(chunk_size=1024):
                    imageFile.write(chunk)
        except Exception as e:
            print "unable to save image: {0}".format(e)


