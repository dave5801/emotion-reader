"""Test Facial Image Verification."""

from django.test import TestCase
from django.test import RequestFactory
from emotion_authentication.models import FaceVerificationManager
from django.conf import settings
from emotion_authentication.face_verification import FaceVerification
import os
from emotion_profile.tests import UserFactory
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from emotion_profile.models import User
from django.core.urlresolvers import reverse_lazy
from unittest.mock import patch

filepath = "nicholas_cage"
full_path = os.path.join(settings.BASE_DIR,'emotion_authentication/' + filepath)


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
        patcher = patch('cognitive_face.util.request', return_value=[{'faceId': 'xxxxx'}])
        patcher.start()
        self.addCleanup(patcher.stop)

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
        self.request = RequestFactory()
        self.request.user = self.user

    def test_create_face_verification_object(self):
        '''test if face verification object is created.'''
        self.assertIsNotNone(self.user.faces)

    def test_new_user_face_verification_return_no_reg_photo(self):
        """test if fvo invalid."""
        self.assertIsNone(self.user.faces.auth_face_id)
        self.assertIsNone(self.user.faces.auth_last_recorded)

        
    def test_new_user_set_face_image_for_auth_return_valid(self):
        '''Test for valid object returns.'''
        filepath = "nicholas_cage" #This is a test directory with gag photos.
        full_path = os.path.join(settings.BASE_DIR, 'emotion_authentication/' + filepath)

        test_face_verifier = FaceVerificationManager.objects.get(user=self.user)
        with open(os.path.join(full_path, 'cage1.png'), 'rb') as f:
            content = f.read()
        test_face_verifier.auth_face = SimpleUploadedFile(name="cage1",
                                                     content=content,
                                                     content_type="image/png"
                                                     )
        test_face_verifier.auth_face_id = 'xxxxxxxxxxx'
        test_face_verifier.auth_last_recorded = timezone.now()
        test_face_verifier.save()
        user = User.objects.get(username=self.user.username)

        self.assertIsNotNone(user.faces.auth_face_id)
        self.assertIsNotNone(user.faces.auth_last_recorded)


class FaceVerificationViewTests(TestCase):
    """Tests if authentication pages route properly."""

    def setUp(self):
        """"user and mock api calls."""
        user = UserFactory.create(username='bob')
        user.set_password('password')
        user.save()
        self.user = user
        patcher = patch('cognitive_face.util.request', return_value={0: {'faceId': 'xxxxx'}, 'isIdentical': True})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_route_to_face_auth(self):
        """test if registration routes to face auth."""
        with open(os.path.join(full_path, 'cage1.png'), 'rb') as f:
            content = f.read()#create file from file path

        self.user.faces.auth_face = SimpleUploadedFile(name="cage1",
                                                     content=content,
                                                     content_type="image/png")
        self.user.faces.save()
        data = {'image': 'data: base64,FAKE'}
        response = self.client.post(reverse_lazy('face_verification'), data)
        self.assertEqual(response.status_code, 302)

    def test_face_registration_post_has_302_response_not_logged_in(self):
        """Test that face reg route has 302 response when not logged in."""
        data = {'image': 'data: base64,FAKE'}
        response = self.client.post(reverse_lazy('face_register_view'), data)
        self.assertEqual(response.status_code, 302)

    def test_face_registration_post_has_200_response_logged_in(self):
        """Test that the face reg route has a 200 response."""
        self.client.login(username='bob', password='password')

        patcher = patch('cognitive_face.util.request', return_value=[{'faceId': 'xxxxx'}])
        patcher.start()
        self.addCleanup(patcher.stop)

        data = {'image': 'data: base64,FAKE'}
        response = self.client.post(reverse_lazy('face_register_view'), data)
        self.assertEqual(response.status_code, 200)

    def test_face_registration_post_sets_auth_face_id(self):
        """Test that the face reg route sets the face id."""
        self.client.login(username='bob', password='password')

        patcher = patch('cognitive_face.util.request', return_value=[{'faceId': 'xxxxx'}])
        patcher.start()
        self.addCleanup(patcher.stop)

        data = {'image': 'data: base64,FAKE'}
        self.client.post(reverse_lazy('face_register_view'), data)

        verifier = FaceVerificationManager.objects.get(user=self.user)
        self.assertEqual(verifier.auth_face_id, 'xxxxx')
        self.assertEqual(verifier.auth_last_recorded.second, timezone.now().second)
