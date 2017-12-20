'use strict';

var app = app || {};

(function(module) {

    let video = document.querySelector('video');
    let canvas = document.querySelector('canvas');
    let ctx = canvas.getContext('2d');
    let localMediaStream = null;

    function savePhoto(dataURL) {
        $.post('/emotions/record', {
            image: dataURL,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        }).fail(console.error)
    }

    function snapshot() {
      if (localMediaStream) {
        let image = localMediaStream.getVideoTracks()[0].getSettings();
        let xRatio = canvas.width / image.width;
        let yRatio = canvas.height / image.height;
        let ratio = Math.min(xRatio, yRatio);

        ctx.drawImage(video, 0, 0, image.width, image.height,
                             0, 0, image.width * ratio, image.height * ratio);

        video.pause();
        localMediaStream.getVideoTracks()[0].stop();
        savePhoto(canvas.toDataURL('image/jpeg'))
        $('#capture').hide();
      }
    }

    function startCamera() {
        navigator.mediaDevices.getUserMedia({video: true})
        .then(stream => {
          video.src = window.URL.createObjectURL(stream);
          localMediaStream = stream;
          $('#start-camera').hide();
          $('#capture').show();
        })
        .catch(console.error);
    }

    app.setupImageCap = function() {
        $('#capture').hide();
        $('#start-camera').on('click', startCamera)
        $('#capture').on('click', snapshot) 
    }

})(app);