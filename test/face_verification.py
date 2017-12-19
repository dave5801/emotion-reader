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

class FaceVerificationObject(object):
    """Face Verification Object."""
    def __init__(self, filepath_for_faces=None, face_to_verify=None):
        self.filepath_for_faces = filepath_for_faces
        self.face_to_verify = face_to_verify

        self.faceID = None

    def get_faces_from_dir(self):
        """Get Directory of Faces."""
        if not os.path.isdir(self.filepath_for_faces):
            return "Invalid File Path"

        return [f for f in listdir(self.filepath_for_faces) if isfile(join(self.filepath_for_faces, f))]

    def check_valid_face_file(self, face_file):
        """Validate an individual face image."""

        face_image_file_path = self.filepath_for_faces + "/" +face_file

        face_image_file = Path(face_image_file_path)

        return face_image_file.exists()


'''
    def detected(image, face_id=True, landmarks=False, attributes=''):
        return None

    def verified(face_id, another_face_id=None, person_group_id=None,
           person_id=None)
        return None

    def grouped(list_of_face_ids):
        return None'''

if __name__ == '__main__':

    file_dir = "nicholas_cage"

    fvo = FaceVerificationObject(file_dir)

    list_of_faces = fvo.get_faces_from_dir()
    print(list_of_faces)

    #valid_face_file = fvo.check_valid_face_file(list_of_faces[0])
    valid_face_file = fvo.check_valid_face_file("badfile.png")
    print(valid_face_file) 