from django.views.generic import TemplateView
from base64 import b64decode
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from emotion_authentication.models import FaceVerificationManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import  login
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone

# Create your views here.


'''
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
'''


class FaceVerificationView(TemplateView):

    template_name = 'emotion_authentication/face_verification.html'

    def post(self, request, *args, **kwargs):
        """Extract emotions from posted image."""
        try:
            image = request.POST['image'].split(',', maxsplit=1)[1]
            image = b64decode(image)
        except (KeyError, IndexError):
            return HttpResponseBadRequest('Invalid data.')

        reg_face_verifier = FaceVerificationManager.objects.first()

        new_face = reg_face_verifier.detected(image, img_stream=True)[0]['faceId']

        for verifier in FaceVerificationManager.objects.all():

            reg_face_verification = verifier.verify_against_registration(new_face)

            if reg_face_verification is True:
                break
        else:
            return HttpResponseBadRequest('Face Verification Error.')

        if verifier.user.is_active:
            login(request, verifier.user)
            return redirect('profile')
        else:
            return HttpResponseBadRequest('Login Failed')


class FaceCaptureAndSaveView(LoginRequiredMixin, TemplateView):

    template_name = 'emotion_authentication/face_register.html'

    def post(self, request, *args, **kwargs):
        """Extract emotions from posted image."""
        try:
            image = request.POST['image'].split(',', maxsplit=1)[1]
            image = b64decode(image)
        except (KeyError, IndexError):
            return HttpResponseBadRequest('Face Verification Error.')

        face_verifier = FaceVerificationManager.objects.get(user=request.user)

        faces = face_verifier.detected(image, img_stream=True)

        if len(faces) != 1:
            return HttpResponseBadRequest('Invalid number of faces')

        face_verifier.auth_face = SimpleUploadedFile(name="auth_face.jpg",
                                                     content=image,
                                                     content_type="image/jpeg"
                                                     )
        face_verifier.auth_face_id = faces[0]['faceId']
        face_verifier.auth_last_recorded = timezone.now()

        face_verifier.save()

        return HttpResponse('Face Verified')
