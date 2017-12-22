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
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

filepath = "nicholas_cage"
full_path = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + filepath)

'''
TEST_REG_PHOTO = SimpleUploadedFile(name='cage1', 
    content=open(os.path.join(full_path,'cage1.png'), 'rb').read(), content_type='image/png')

TEST_NEW_PHOTO = SimpleUploadedFile(name='cage2',
 content=open(os.path.join(full_path,'cage2.png'), 'rb').read(), content_type='image/png')
'''

class FaceDetectionTests(TestCase):
    """Test Basic Face Detection."""

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
        verify = FaceVerification(filepath_for_faces=full_path)
        x = verify.detected('cage1.png')
        self.assertEqual(len(x), 1)


    def test_no_face_detected(self):
        """Test bad directory, no face detected."""
        verify = FaceVerification(filepath_for_faces=full_path)
        x = verify.detected()
        self.assertEqual(x, False)


class FaceVerificationTests(TestCase):
    """Test if User can be authenticated."""
        
    def setUp(self):
        user = UserFactory.create()
        user.set_password(factory.Faker('password'))
        user.save()
        self.user = user

    def test_create_face_verification_object(self):
        '''test if face verification object is created.'''
        self.assertIsNotNone(self.user.faces)

    def test_face_verification_valid(self):
        """test if fvo valid."""
        self.assertIsNotNone(self.user.faces.auth_face)
        self.assertIsNotNone(self.user.faces.auth_face_id)
        self.assertIsNotNone(self.user.faces.auth_last_recorded)

       
        #test if fvo not valid with bad picture
        #test new user, registration photo does not exist
        #test current user, registration photo exists
        #test if current user is verified

class FaceVerificationViewTests(TestCase):
    """Tests if authentication pages work properly."""

    def setUp(self):
        client = Client()
        user = UserFactory.create()
        user.set_password(factory.Faker('password'))
        user.save()

        #test if login routes face verification view
    def test_profile_route_accessible_when_logged_in(self):
        """Test that a user can only see their profile page if logged in."""
        self.client.login(username='dan', password='password')
        response = self.client.get(reverse_lazy('face_verification'))
        self.assertEqual(response.status_code, 200)
        
        #test if registration view routes to verification view

