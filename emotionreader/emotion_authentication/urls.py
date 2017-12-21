from django.conf.urls import url, include
from emotion_authentication.views import FaceVerificationView, FaceCaptureAndSaveView


urlpatterns = [
    url(r'^$', FaceVerificationView.as_view(), name="face_verification"),
    url(r'^register$', FaceCaptureAndSaveView.as_view(), name="face_register_view")
]