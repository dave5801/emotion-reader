"""Test Facial Image Verification."""

#test image is not verified is false, cage and travolta
#test image is verified, cage and cage
#test grouping happened, one messy group
#test grouping, no messy group
from django.conf import settings
from emotion_authentication.face_verification import FaceVerification
import os
FILEPATH = "nicholas_cage"
FULL_PATH = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + FILEPATH)
verify = FaceVerification(filepath_for_faces=FULL_PATH)
TEST_FACE_LIST = verify.get_faces_from_dir()


def test_select_from_face_dir():
    """Test faces are selected from valid directory."""
    filepath = "nicholas_cage"
    full_path = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + filepath)
    verify = FaceVerification(filepath_for_faces=full_path)
    x = verify.get_faces_from_dir()
    assert x is not None


def test_select_from_face_dir_invalid_dir():
    """Test attempt to select from invalid directory."""
    filepath = "thisIsaBadDirectory"
    full_path = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + filepath)
    verify = FaceVerification(filepath_for_faces=full_path)
    x = verify.get_faces_from_dir()
    assert x == "Invalid File Path"


def test_face_detected():
    """Test face is detected."""
    verify = FaceVerification(filepath_for_faces=FULL_PATH)
    x = verify.detected(os.path.join(FULL_PATH, TEST_FACE_LIST[0]))
    assert x is not None


def test_no_face_detected():
    """Test bad directory, no face detected."""
    verify = FaceVerification(filepath_for_faces=FULL_PATH)
    x = verify.detected(os.path.join('badFilePath', TEST_FACE_LIST[0]))

    assert x == "Invalid File"

'''
'''
# def test_two_faces_verified():
#     verify = FaceVerification(filepath_for_faces=FULL_PATH)
#     x = verify.detected(os.path.join(FULL_PATH, TEST_FACE_LIST[0]))
#     y = verify.detected(os.path.join(FULL_PATH, TEST_FACE_LIST[1]))
#     from face_off import verify, detect

#     x = detect(FILEPATH + "/" + TEST_FACE_LIST[0])
#     y = detect(FILEPATH + "/" + TEST_FACE_LIST[1])
#     test_verify = verify(x[0]['faceId'],y[0]['faceId'])
#     assert test_verify['isIdentical'] is True
