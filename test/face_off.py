#https://github.com/Microsoft/Cognitive-Face-Python/tree/master/cognitive_face

import util

def detect(image, face_id=True, landmarks=False, attributes=''):
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

def find_similars(face_id,
                  face_list_id=None,
                  face_ids=None,
                  max_candidates_return=20,
                  mode='matchPerson'):
    """Given query face's `face_id`, to search the similar-looking faces from a
    `face_id` array or a `face_list_id`.
    Parameter `face_list_id` and `face_ids` should not be provided at the same
    time.
    Args:
        face_id: `face_id` of the query face. User needs to call `face.detect`
            first to get a valid `face_id`. Note that this `face_id` is not
            persisted and will expire in 24 hours after the detection call.
        face_list_id: An existing user-specified unique candidate face list,
            created in `face_list.create`. Face list contains a set of
            `persisted_face_ids` which are persisted and will never expire.
        face_ids: An array of candidate `face_id`s. All of them are created by
            `face.detect` and the `face_id`s will expire in 24 hours after the
            detection call. The number of `face_id`s is limited to 1000.
        max_candidates_return: Optional parameter. The number of top similar
            faces returned. The valid range is [1, 1000]. It defaults to 20.
        mode: Optional parameter. Similar face searching mode. It can be
            "matchPerson" or "matchFace". It defaults to "matchPerson".
    Returns:
        An array of the most similar faces represented in `face_id` if the
        input parameter is `face_ids` or `persisted_face_id` if the input
        parameter is `face_list_id`.
    """
    url = 'findsimilars'
    json = {
        'faceId': face_id,
        'faceListId': face_list_id,
        'faceIds': face_ids,
        'maxNumOfCandidatesReturned': max_candidates_return,
        'mode': mode,
    }

    return util.request('POST', url, json=json)


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

if __name__ == '__main__':

    from select_from_face_dir import select_from_face_dir

    cage_dir = "nicholas_cage"

    image_contents = select_from_face_dir(cage_dir)
    print(image_contents)

    face_id_list = []

    for i in image_contents:
        temp_url = cage_dir + "/" + i
        face_id_list.append(detect(temp_url))

    print(face_id_list)

    #formatted_faces = []

    for j in face_id_list:
        print(j[0])
        #print(verify(j[0]))

x = {'faceId': 'de9ca459-f0bc-4b20-a66b-54e352d6747c', 'faceRectangle': {'top': 134, 'left': 240, 'width': 204, 'height': 204}}
y = {'faceId': '74ac125d-059f-4fac-849f-2d65871906c0', 'faceRectangle': {'top': 152, 'left': 57, 'width': 212, 'height': 212}}

z = verify(x['faceId'],y['faceId'])
print(z)
