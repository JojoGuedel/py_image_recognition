import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import requests
import shutil
from PIL import Image, ImageDraw, ImageFont

import draw
import converter

IMAGE = 'https://www.vmcdn.ca/f/files/victoriatimescolonist/json/2022/03/web1_vka-viewstreet-13264.jpg'
KEY = 'ddb26f4091604a8ab5a2872a82403846'

def download(image_url):
    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open('./data/image.jpg','wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully downloaded')
    else:
        print('Image Couldn\'t be retreived')

def main():
    download(IMAGE)

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'visualFeatures': 'Objects',
        # 'details': 'Landmarks',
        'language': 'en',
    })

    body = '{"url": "%s"}' % IMAGE

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", f"/vision/v3.0/analyze?{params}", body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        root = converter.Root.from_dict(json.loads(data))
        objects = root.objects

        with Image.open("./data/image.jpg") as im:
            draw = ImageDraw.Draw(im)
            draw.line((0, 0) + im.size, fill=128)
            draw.line((0, im.size[1], im.size[0], 0), fill=128)

            for i in objects:
                shape = [(i.rectangle.x, i.rectangle.y), (i.rectangle.x + i.rectangle.w, i.rectangle.y + i.rectangle.h)]
                draw.rectangle(shape, outline='red', width=5)
                draw.text((i.rectangle.x, i.rectangle.y), text=i.object, font=ImageFont.truetype('arial.ttf', 50))

            im.show()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
    main()