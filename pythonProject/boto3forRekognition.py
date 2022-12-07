import boto3
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


f_img = 'IMG_7289.jpg'
in_img = Image.open(f_img)
w, h = in_img.size

# r_obj = boto3.client('rekognition')
# with open(f_img, 'rb') as file:
#     r_out = r_obj.detect_faces(
#     Image={'Bytes': file.read()}
#     )
r_obj = boto3.client('rekognition')
with open(f_img, 'rb') as file:
    r_out = r_obj.detect_faces(
        Image={'Bytes': file.read()},
        Attributes=['ALL']
    )
    print(json.dumps(r_out, indent=2))

draw = ImageDraw.Draw(in_img)
emotionType = "HAPPY"
score = 0

for face in r_out['FaceDetails']:
    box = face['BoundingBox']
    left = int(box['Left']*w)
    top = int(box['Top']*h)
    width = int(box['Width']*w)
    height = int(box['Height']*h)
    draw.rectangle([(left, top), (left + width, top + height)], outline='lime', width=2)
    for mark in face['Landmarks']:
        x = int(mark['X']*w)
        y = int(mark['Y']*h)
        draw.ellipse(((x, y), (x + 3, y + 3)), fill='white', outline='white')

    for emotion in face['Emotions']:
        if int(emotion['Confidence']) > score:
            score = int(emotion['Confidence'])
            emotionType = str(emotion['Type'])
    #draw.text((1,1), emotionType, 'red', font=ImageFont.truetype('Arial.ttf', 150))

    draw.text((left, top-30), emotionType, 'red', font=ImageFont.truetype('Arial.ttf', 30))

in_img.save('show_' + f_img)
in_img.show()

