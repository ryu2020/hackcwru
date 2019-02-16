from PIL import Image
import base64
import requests
import json
import csv
import glob
import datetime
import key
from dateutil import parser

API_KEY = key.apikey()

def sentiment(json):
    r = requests.post('https://language.googleapis.com/v1/documents:analyzeSentiment' + API_KEY, json = json)
    return r

def ocr(json):
    r = requests.post('https://vision.googleapis.com/v1/images:annotate' + API_KEY, data = json)
    #print(r.text)
    #r = r.json()
    return r

def makeImageJSON(image):
    #image = {"content": encode_image(image)}
    features = [{"type": "DOCUMENT_TEXT_DETECTION", "maxResults":0}]
    return {"image":{"source":{"imageUri":"https://www.wikihow.com/images/thumb/0/01/Write-a-Journal-Entry-Step-14.jpg/aid171876-v4-728px-Write-a-Journal-Entry-Step-14.jpg"}}, "features":features}

def makeTextJSON(text):
    return {"document": {"type":"PLAIN_TEXT", "content":text}, "encodingType": "UTF32"}

def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content)

def getImages():
    image_list = []
    for filename in glob.glob('C:/users/Bert/workspace/hackcwru/images/*'):
        image_content = open(filename, 'rb').read()
        image_list.append(str(base64.b64encode(image_content)))
    return image_list


reqs = []
imagearr = getImages()
#print(imagearr)
for image in imagearr:
    reqs.append(makeImageJSON(image))

def parsedatetime(string):
    cleaned = string.replace(" ", "")
    date = parser.parse(cleaned, fuzzy = True, dayfirst = False)
    return date

req = json.dumps({"requests": reqs})
read = ocr(req).json()
for response in read["responses"]:
    text = response["fullTextAnnotation"]["text"].replace("\n", " ")

    sen = sentiment(makeTextJSON(text)).json()
    sentuple = (sen["documentSentiment"]["score"],sen["documentSentiment"]["magnitude"], parsedatetime(text))

print(sentuple)
