"""Test Facial Image Verification."""

#test image is not verified is false, cage and travolta
#test image is verified, cage and cage
#test grouping happened, one messy group
#test grouping, no messy group
from select_from_face_dir import select_from_face_dir
FILEPATH = "nicholas_cage"
TEST_FACE_LIST = select_from_face_dir(FILEPATH)



def test_select_from_face_dir():
    from select_from_face_dir import select_from_face_dir

    filepath = "nicholas_cage"
    x = select_from_face_dir(filepath)
    assert x != None


def test_select_from_face_dir_invalid_dir():
    from select_from_face_dir import select_from_face_dir

    filepath = "thisIsaBadDirectory"
    x = select_from_face_dir(filepath)
    assert x == "Invalid File Path"


def test_face_detected():
    from face_off import detect

    x = detect(FILEPATH + "/" +TEST_FACE_LIST[0])
    assert x != None

