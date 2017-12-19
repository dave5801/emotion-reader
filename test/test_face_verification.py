"""Test Facial Image Verification."""

#test image is not verified is false, cage and travolta
#test image is verified, cage and cage
#test grouping happened, one messy group
#test grouping, no messy group
from select_from_face_dir import select_from_face_dir
FILEPATH = "nicholas_cage"
TEST_FACE_LIST = select_from_face_dir(FILEPATH)



def test_select_from_face_dir():
    """Test faces are selected from valid directory."""
    from select_from_face_dir import select_from_face_dir

    filepath = "nicholas_cage"
    x = select_from_face_dir(filepath)
    assert x != None


def test_select_from_face_dir_invalid_dir():
    """Test attempt to select from invalid directory."""
    from select_from_face_dir import select_from_face_dir

    filepath = "thisIsaBadDirectory"
    x = select_from_face_dir(filepath)
    assert x == "Invalid File Path"


def test_face_detected():
    """Test face is detected."""
    from face_off import detect

    x = detect(FILEPATH + "/" + TEST_FACE_LIST[0])
    print("TEST", x)
    assert x != None


def test_no_face_detected():
    """Test bad directory, no face detected."""
    from face_off import detect

    x = detect("badFilePath" + "/" + TEST_FACE_LIST[0])
    assert x == "Invalid File Path"
'''
def test_two_faces_verified():
    from face_off import verify, detect

    print(TEST_FACE_LIST[0], TEST_FACE_LIST[1])
    x = detect(FILEPATH + "/" + TEST_FACE_LIST[0])
    y = detect(FILEPATH + "/" + TEST_FACE_LIST[1])
    print(x)'''