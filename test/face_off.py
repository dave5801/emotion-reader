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


if __name__ == '__main__':
    img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    response = detect(img_url)
    print("RESPONSE", response)