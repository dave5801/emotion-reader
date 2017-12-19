#https://github.com/Microsoft/Cognitive-Face-Python/tree/master/cognitive_face

import util
import os
from pathlib import Path

def detect(image, face_id=True, landmarks=False, attributes=''):

    image_file = Path(image)

    if not image_file.exists():
        return "Invalid File"


    """Detect human faces in an image and returns face locations, and
    optionally with `face_id`s, landmarks, and attributes.
    Args:
        image: A URL or a file path or a file-like object represents an image.
        face_id: [Optional] Return faceIds of the detected faces or not. The
            default value is true.
        landmarks: [Optional] Return face landmarks of the detected faces or
            not. The default value is false.
        attributes: [Optional] Analyze and return the one or more specified
            face attributes in the comma-separated string like
            "age,gender". Supported face attributes include age, gender,
            headPose, smile, facialHair, glasses and emotion.
            Note that each face attribute analysis has additional
            computational and time cost.
    Returns:
        An array of face entries ranked by face rectangle size in descending
        order. An empty response indicates no faces detected. A face entry may
        contain the corresponding values depending on input parameters.
    """

    url = 'detect'
    headers, data, json = util.parse_image(image)
    params = {
        'returnFaceId': face_id and 'true' or 'false',
        'returnFaceLandmarks': landmarks and 'true' or 'false',
        'returnFaceAttributes': attributes,
    }

    return util.request(
        'POST', url, headers=headers, params=params, json=json, data=data)


def verify(face_id, another_face_id=None, person_group_id=None,
           person_id=None):
    """Verify whether two faces belong to a same person or whether one face
    belongs to a person.
    For face to face verification, only `face_id` and `another_face_id` is
    necessary. For face to person verification, only `face_id`,
    `person_group_id` and `person_id` is needed.
    Args:
        face_id: `face_id` of one face, comes from `face.detect`.
        another_face_id: `face_id` of another face, comes from `face.detect`.
        person_group_id: Using existing `person_group_id` and `person_id` for
            fast loading a specified person. `person_group_id` is created in
            `person_group.create`.
        person_id: Specify a certain person in a person group. `person_id` is
            created in `person.create`.
    Returns:
        The verification result.
    """
    url = 'verify'
    json = {}
    if another_face_id:
        json.update({
            'faceId1': face_id,
            'faceId2': another_face_id,
        })
    else:
        json.update({
            'faceId': face_id,
            'personGroupId': person_group_id,
            'personId': person_id,
        })

    return util.request('POST', url, json=json)


def group(face_ids):
    """Divide candidate faces into groups based on face similarity.
    Args:
        face_ids: An array of candidate `face_id`s created by `face.detect`.
            The maximum is 1000 faces.
    Returns:
        one or more groups of similar faces (ranked by group size) and a
        messyGroup.
    """
    url = 'group'
    json = {
        'faceIds': face_ids,
    }

    return util.request('POST', url, json=json)

if __name__ == '__main__':


    bad = "nicholas_cage/cage10.png"

    from select_from_face_dir import select_from_face_dir

    cage_dir = "nicholas_cage"

    image_contents = select_from_face_dir(cage_dir)

    faces_detected = []

    for i in image_contents:
        temp_url = cage_dir + "/" + i
        print(temp_url)
        faces_detected.append(detect(temp_url))

    print(faces_detected)

    '''VERIFY IS GOOD
    for j in range(len(faces_detected)-1):
        x = faces_detected[j][0]['faceId']
        y = faces_detected[j+1][0]['faceId']
        print(verify(x,y))

    face_id_list = []

    for k in faces_detected:
        face_id_list.append(k[0]['faceId'])

    print(group(face_id_list))'''

