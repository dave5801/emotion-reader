"""Class which facial recognition in authenticion."""

'''
IMAGE CAPTURE - HOW MANY FRAMES PER UNIT OF TIME???
'''

'''
TEST IDEAS:
test if object created
test if object created valid
test if object created invalid
test if dir is valid
test if dir contains invalid file

'''

import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import emotion_authentication.util as util
import cognitive_face as CF
from emotion_authentication.util import Key, BaseUrl

class FaceVerification(object):
    """Face Verification Object."""
    def __init__(self, filepath_for_faces=None, face_to_verify=None):
        self.filepath_for_faces = filepath_for_faces
        self.face_to_verify = face_to_verify

        self.faceID = None

    def format_face_file(self, face_file):
        """formats file: path/to/file.png."""
        return self.filepath_for_faces + "/" +face_file

    def get_faces_from_dir(self):
        """Get Directory of Faces."""
        if not os.path.isdir(self.filepath_for_faces):
            return "Invalid File Path"

        return [f for f in listdir(self.filepath_for_faces) if isfile(join(self.filepath_for_faces, f))]

    def check_valid_face_file(self, face_file):
        """Validate an individual face image."""

        #face_image_file_path = self.format_face_file(face_file)
        print(face_file)
        face_image_file = Path(face_file)

        return face_image_file.exists()


    def detected(self, image, face_id=True, landmarks=False, attributes='', img_stream=False):
        """Returns the ID of a detected face."""

        url = 'detect'
        if not img_stream:

            face_to_detect = self.format_face_file(image)

            if self.check_valid_face_file(face_to_detect) == False:
                print("Invalid Face")
                return False
            headers, data, json = util.parse_image(face_to_detect)
        else:
            headers = {'Content-Type': 'application/octet-stream'}
            data = image
            json = None

        params = {
            'returnFaceId': face_id and 'true' or 'false',
            'returnFaceLandmarks': landmarks and 'true' or 'false',
            'returnFaceAttributes': attributes,
        }


        detection = util.request(
            'POST', url, headers=headers, params=params, json=json, data=data)
        print("DETECTION:",detection)

        #NOTE - this is how you get valid faceIDs --> detection[0]['faceId']

        return detection

    '''Note: Not used currently, will be at later time.'''    
    def group_verify(self,face_id,list_of_face_ids):
        """Any face image found in 'messy groud' is not verified."""
        url = 'group'
        json = {
            'faceIds': list_of_face_ids,
        }

        grouping = util.request('POST', url, json=json)
        
        primary_group = grouping['groups'][0]
        messy_group = grouping['messyGroup']

        if face_id in primary_group:
            return True
        elif face_id in messy_group:
            return False
        else:
            return False

    def verify_against_registration(self, face_id=None, person_group_id=None,
           person_id=None):
        """Check new photo against photo used at registration."""

        #current value is placeholder, this variable will come from a DB query from User Profile
        #registration photo is the initial photo
        registration_photo_id = self.detected("cage1.png")[0]['faceId']

        url = 'verify'
        json = {}
        if registration_photo_id:
            json.update({
                'faceId1': face_id,
                'faceId2': registration_photo_id,
            })
        else:
            json.update({
                'faceId': face_id,
                'personGroupId': person_group_id,
                'personId': person_id,
            })

        registration_verification = util.request('POST', url, json=json)

        print(registration_verification)

        return registration_verification['isIdentical']

    def verifiy_new_user_face(self, face_url):
        CF.Key.set(Key.get())
        CF.BaseUrl.set(BaseUrl.get())
        faces = CF.face.detect(img_url)
        #print(faces[0]['faceRectangle'])
        if not faces:
            return False
        return True


if __name__ == '__main__':

    file_dir = "nicholas_cage"

    fvo = FaceVerification(file_dir)

    list_of_faces = fvo.get_faces_from_dir()
    #print(list_of_faces)

    ''''''
    #valid_face_file = fvo.check_valid_face_file("cage1.png")
    #print(valid_face_file)
    valid_face_file = fvo.detected("cage1.png")[0]['faceId']
    print(valid_face_file)

    
    '''detected_faces = []

    for i in list_of_faces:
        detected_faces.append(fvo.detected(i))

    print(detected_faces)'''

    #x = fvo.group_verify(detected_faces)
    #print("GROUPS", x['groups'][0])
    #print("MESSY GROUP", x['messyGroup'][0])

    #x = fvo.group_verify(detected_faces[0], detected_faces)
    #print(x)

    #registration_photo_id = fvo.detected("cage1.png")
    #print(registration_photo_id) 
    
    #x = fvo.verify_against_registration(detected_faces[0])
    #travolta = fvo.detected("travolta1.png")
    #x = fvo.verify_against_registration(travolta)
    #print(x)

    #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    #img_url = 'not_face.png'
    #single_face = fvo.verifiy_new_user_face(img_url)
    #print(single_face)

    #face2 = "cage1.png"
    #face1 = fvo.detected("cage_and_other_person.png")
    #x = fvo.verify_against_registration(face1)
    #print(x)
