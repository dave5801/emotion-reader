"""Sample API Call for Microsoft Face API."""

import os
import cognitive_face as CF
from util import Key, BaseUrl
'''
def face_call(img_url):
    """Call Face API."""
    face_api_key = os.environ['FACE_API_KEY']
    CF.Key.set(face_api_key)
    CF.BaseUrl.set('https://westcentralus.api.cognitive.microsoft.com/face/v1.0/')

    faces = CF.face.detect(img_url)
    return faces
'''

def face_call(img_url):
    CF.Key.set(Key.get())
    CF.BaseUrl.set(BaseUrl.get())
    faces = CF.face.detect(img_url)
    #print(faces[0]['faceRectangle'])
    print(faces)
    if not faces:
        return False
    return True

if __name__ == '__main__':
    #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    #img_url = 'not_face.png'
    img_url = 'two_faces.png'
    single_face = face_call(img_url)
    print(single_face)
    