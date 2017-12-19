"""."""
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import simplejson as json
import os
from emotion_emotions.models import Emotion


headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.environ.get('EMOTION_API_KEY', '')
}

params = urllib.parse.urlencode({
})

body = "{ 'url': 'https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/16998192_10211730567116496_9207760856371247359_n.jpg?oh=6e0934fb6c28dc40bdaaa52e98cef0c5&oe=5ABDE089' }"

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    parsed = json.loads(data)

    emotion = Emotion(User=self.request.user)
    emotion.anger = parsed[0]['scores']['anger']
    emotion.contempt = parsed[0]['scores']['contempt']
    emotion.disgust = parsed[0]['scores']['disgust']
    emotion.fear = parsed[0]['scores']['fear']
    emotion.happiness = parsed[0]['scores']['happiness']
    emotion.neutral = parsed[0]['scores']['neutral']
    emotion.sadness = parsed[0]['scores']['sadness']
    emotion.surprise = parsed[0]['scores']['surprise']
    emotion.save()

    conn.close()
except Exception as e:
    print(e.args)
