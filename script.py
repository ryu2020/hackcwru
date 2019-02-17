from PIL import Image
import base64
import requests
import json
import csv
import glob
import datetime
from .key import apikey, dropboxkey
import dropbox
from dateutil import parser

API_KEY = apikey()
DROPBOX_KEY = dropboxkey()

def sentiment(json):
    r = requests.post('https://language.googleapis.com/v1/documents:analyzeSentiment' + API_KEY, json = json)
    return r

def ocr(json):
    r = requests.post('https://vision.googleapis.com/v1/images:annotate' + API_KEY, data = json)
    #print(r.text)
    #r = r.json()
    return r

def makeImageJSON(url):
    #image = {"content": encode_image(image)}
    features = [{"type": "DOCUMENT_TEXT_DETECTION", "maxResults":0}]
    return {"image":{"source":{"imageUri":url}}, "features":features}

def makeImageJSONs(content):
    #image = {"content": encode_image(image)}
    features = [{"type": "DOCUMENT_TEXT_DETECTION", "maxResults":0}]
    return {"image":{"content":content}, "features":features}

def makeTextJSON(text):
    return {"document": {"type":"PLAIN_TEXT", "content":text}, "encodingType": "UTF32"}

def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content)

def upload_image(file, path):
    dbx = dropbox.Dropbox(DROPBOX_KEY)
    #print(dbx.users_get_current_account())
    file = image_content = open(file, 'rb')
    image_content = file.read()
    dbx.files_upload(image_content, path,mode=dropbox.files.WriteMode.overwrite)

    result = dbx.files_get_temporary_link(path)
    return result

def getImages():
    image_list = []
    for filename in glob.glob('C:/users/Bert/workspace/hackcwru/images/*'):
        image_content = open(filename, 'rb').read()
        encoded = str(base64.b64encode(image_content))
        image_list.append(encoded)
    return image_list

def write(arr):
    with open('tab.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(arr)

def main(file):

    #result = upload_image(file, "upload.jpg")

    reqs = []
    #reqs.append(makeImageJSON(result.link))

    reqs.append(makeImageJSON(file))

    def parsedatetime(string):
        cleaned = string.replace(" ", "")
        date = parser.parse(cleaned, fuzzy = True, dayfirst = False)
        return date

    req = json.dumps({"requests": reqs})
    read = ocr(req).json()
    #print(read.text)
    tuples = []
    for response in read["responses"]:
        #print(response)
        text = response["fullTextAnnotation"]["text"].replace("\n", " ")

        sen = sentiment(makeTextJSON(text)).json()
        sentuple = (sen["documentSentiment"]["score"],sen["documentSentiment"]["magnitude"], parsedatetime(text))
        tuples.append(sentuple)

    arr = [sentuple[2].month, sentuple[2].day, sentuple[2].year, sentuple[0], sentuple[1]]
    write(arr)
    return str(arr)
