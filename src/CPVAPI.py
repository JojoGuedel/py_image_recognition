import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

class Metadata:
    def __init__(self, height, width, format):
        self.height = height
        self.width = width
        self.format = format

    @staticmethod
    def from_dict(dict):
        return Metadata(
            int(dict.get("height")), 
            int(dict.get("width")), 
            str(dict.get("format")))

class Rectangle:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def from_dict(dict):
        return Rectangle(
            (int(dict.get("x")), int(dict.get("y"))), 
            (int(dict.get("w")), int(dict.get("h"))))

class Object:
    def __init__(self, rectangle, object, confidence):
        self.rectangle = rectangle
        self.object = object
        self.confidence = confidence

    @staticmethod
    def from_dict(dict):
        return Object(
            Rectangle.from_dict(dict.get("rectangle")),
            str(dict.get("object")),
            float(dict.get("confidence")))

class Response:
    def __init__(self, objects, requestID, metadata):
        self.objects = objects
        self.requestId = requestID
        self.metadata = metadata

    @staticmethod
    def from_dict(dict):
        return Response(
            [Object.from_dict(y) for y in dict.get("objects")],
            str(dict.get("requestId")),
            Metadata.from_dict(dict.get("metadata")))

def try_get(image_url, key):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'visualFeatures': 'Objects',
        # 'details': 'Landmarks',
        'language': 'en',
    })

    body = '{"url": "%s"}' % image_url

    try:
        connection = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        connection.request("POST", f"/vision/v3.0/analyze?{params}", body, headers)
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return Response.from_dict(json.loads(data))

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))