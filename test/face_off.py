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

if __name__ == '__main__':
    #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    #response = detect(img_url)
    #face_id = response[0]['faceId']
    
    #print(find_similars(face_id))
    from select_from_face_dir import select_from_face_dir

    cage_dir = "nicholas_cage"

    image_contents = select_from_face_dir(cage_dir)
    print(image_contents)

    face_id_list = []

#add_face(cage_dir + "/" +i,1)
    for i in image_contents:
        temp_url = cage_dir + "/" + i
        face_id_list.append(detect(temp_url))

    print(face_id_list)
