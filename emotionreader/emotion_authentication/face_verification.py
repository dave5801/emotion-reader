"""
Face Verification Object

This checks if an individual is recognized by the system
This object is used during the authentication phase.
"""

import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import cognitive_face as CF
from cognitive_face.util import Key, BaseUrl
from django.utils import timezone


class FaceVerification(object):
    """Create Class."""

    def __init__(self, filepath_for_faces=None, face_to_verify=None):
        """Initialization."""
        Key.set(os.environ.get('FACE_API_KEY1', ''))
        BaseUrl.set(os.environ.get('FACE_URL', ''))

        self.filepath_for_faces = filepath_for_faces
        self.face_to_verify = face_to_verify

        self.faceID = None

    def format_face_file(self, face_file):
        """Format file: path/to/file.png."""
        return self.filepath_for_faces + "/" + face_file

    def get_faces_from_dir(self):
        """Get Directory of Faces."""
        if not os.path.isdir(self.filepath_for_faces):
            return "Invalid File Path"

        return [f for f in listdir(self.filepath_for_faces) if isfile(join(self.filepath_for_faces, f))]

    def check_valid_face_file(self, face_file):
        """Validate an individual face image."""
        face_image_file = Path(face_file)

        return face_image_file.exists()

    def detected(self, image=None, face_id=True, landmarks=False, attributes='', img_stream=False):
        """Returns the ID of a detected face."""
        if not image:
            return False

        url = 'detect'
        if not img_stream:

            face_to_detect = self.format_face_file(image)

            if self.check_valid_face_file(face_to_detect) is False:

                print("Invalid Face")
                return False
            headers, data, json = CF.util.parse_image(face_to_detect)

        else:
            headers = {'Content-Type': 'application/octet-stream'}
            data = image
            json = None

        params = {
            'returnFaceId': face_id and 'true' or 'false',
            'returnFaceLandmarks': landmarks and 'true' or 'false',
            'returnFaceAttributes': attributes,
        }

        detection = CF.util.request(
            'POST', url, headers=headers, params=params, json=json, data=data)

        return detection

    '''NOTE: This is not in use currently, but will be useful later.'''
    def group_verify(self, face_id, list_of_face_ids):
        """Find individual by comparing across groups."""
        url = 'group'
        json = {
            'faceIds': list_of_face_ids,
        }

        """Any face image found in 'messy groud' is not verified."""
        grouping = CF.util.request('POST', url, json=json)
        primary_group = grouping['groups'][0]
        messy_group = grouping['messyGroup']

        if face_id in primary_group:
            return True
        elif face_id in messy_group:
            return False
        else:
            return False

    def verify_against_registration(self, face_id=None, person_group_id=None, person_id=None):
        """Check new photo against photo used at registration."""
        face_now = timezone.now()

        if hasattr(self, 'auth_face') and self.auth_face:

            if self.auth_last_recorded:
                time_delta = face_now - self.auth_last_recorded
                old_id = time_delta.days >= 1

            else:
                old_id = True

            if old_id:

                reg_image = self.auth_face.file.file.read()
                registration_photo_id = self.detected(reg_image, img_stream=True)[0]['faceId']
                self.auth_face_id = registration_photo_id
                self.auth_last_recorded = timezone.now()
            else:
                registration_photo_id = self.auth_face_id
        else:
            return False

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

        registration_verification = CF.util.request('POST', url, json=json)

        return registration_verification['isIdentical']


if __name__ == '__main__':  # pragma: nocover
    """Basic Usage of Face Verification."""

    file_dir = "nicholas_cage"

    fvo = FaceVerification(file_dir)

    list_of_faces = fvo.get_faces_from_dir()

    valid_face_file = fvo.detected("cage1.png")[0]['faceId']
    print(valid_face_file)
