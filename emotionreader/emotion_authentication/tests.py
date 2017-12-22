"""Test Facial Image Verification."""
#./manage.py test emotion_authentication.tests
from django.test import TestCase
from django.test import TestCase, RequestFactory
from emotion_authentication.models import FaceVerificationManager, create_face_verification_object
from django.conf import settings
from emotion_authentication.face_verification import FaceVerification
import os
from emotion_profile.tests import UserFactory
import factory


FILEPATH = "nicholas_cage"
FULL_PATH = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + FILEPATH)
verify = FaceVerification(filepath_for_faces=FULL_PATH)
TEST_FACE_LIST = verify.get_faces_from_dir()

class FaceAuthenticationTests(TestCase):

    def setUp(self):
        user = UserFactory.create()
        user.set_password(factory.Faker('password'))
        user.save()


    def test_select_from_face_dir(self):
        """Test faces are selected from valid directory."""
        filepath = "nicholas_cage"
        full_path = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + filepath)
        verify = FaceVerification(filepath_for_faces=full_path)
        x = verify.get_faces_from_dir()
        self.assertIsNotNone(x)

    def test_select_from_face_dir_invalid_dir(self):
        """Test attempt to select from invalid directory."""
        filepath = "thisIsaBadDirectory"
        full_path = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + filepath)
        verify = FaceVerification(filepath_for_faces=full_path)
        x = verify.get_faces_from_dir()
        self.assertEqual(x, 'Invalid File Path')


    def test_face_detected(self):
        """Test face is detected."""
        verify = FaceVerification(filepath_for_faces=FULL_PATH)
        x = verify.detected(os.path.join(FULL_PATH, TEST_FACE_LIST[0]))
        self.assertIsNotNone(x)


    def test_no_face_detected(self):
        """Test bad directory, no face detected."""
        verify = FaceVerification(filepath_for_faces=FULL_PATH)
        x = verify.detected(os.path.join('badFilePath', TEST_FACE_LIST[0]))
        self.assertEqual(x, False)
