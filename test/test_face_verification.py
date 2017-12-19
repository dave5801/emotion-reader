#test for dir contents
#test invalid directory

#test image is not verified is false, cage and travolta
#test image is verified, cage and cage
#test grouping happened, one messy group
#test grouping, no messy group

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