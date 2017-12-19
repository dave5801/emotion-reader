"""Class which facial recognition in authenticion."""

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
import util

class FaceVerificationObject(object):
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


    def detected(self, image, face_id=True, landmarks=False, attributes=''):
        """Returns the ID of a detected face."""
        face_to_detect = self.format_face_file(image)

        if self.check_valid_face_file(face_to_detect) == False:
            print("Invalid Face")
            return False

        url = 'detect'
        headers, data, json = util.parse_image(face_to_detect)

        params = {
            'returnFaceId': face_id and 'true' or 'false',
            'returnFaceLandmarks': landmarks and 'true' or 'false',
            'returnFaceAttributes': attributes,
        }


        detection = util.request(
            'POST', url, headers=headers, params=params, json=json, data=data)

        return detection[0]['faceId']


    def grouped(self,list_of_face_ids):
        url = 'group'
        json = {
            'faceIds': list_of_face_ids,
        }

        return util.request('POST', url, json=json)

if __name__ == '__main__':

    file_dir = "nicholas_cage"

    fvo = FaceVerificationObject(file_dir)

    list_of_faces = fvo.get_faces_from_dir()
    print(list_of_faces)

    '''
    valid_face_file = fvo.check_valid_face_file("cage1.png")
    print(valid_face_file)
    valid_face_file = fvo.detected("cage1.png")
    print(valid_face_file)'''

    detected_faces = []

    for i in list_of_faces:
        detected_faces.append(fvo.detected(i))

    print(detected_faces)

    x = fvo.grouped(detected_faces)
    print(x)

    
