'use strict';

var app = app || {};

(function(module) {

    let video = document.querySelector('video');
    let canvas = document.querySelector('canvas');
    let ctx = canvas.getContext('2d');
    let localMediaStream = null;

    let post_success_text = 'Save successful!'
    let post_fail_text = 'Save failed.'

    function savePhoto(dataURL) {
        $.post(location.href, {
            image: dataURL,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        })
        .done(() => {
            $('#saved').text(post_success_text)
        })
        .fail((err) => {
            $('#saved').text(post_fail_text)
        })
    }

    function snapshot() {
      if (localMediaStream) {
        let image = localMediaStream.getVideoTracks()[0].getSettings();
        let xRatio = canvas.width / image.width;
        let yRatio = canvas.height / image.height;
        let ratio = Math.min(xRatio, yRatio);

        ctx.drawImage(video, 0, 0, image.width, image.height,
                             0, 0, image.width * ratio, image.height * ratio);

        let now = new Date(Date.now())
        $('#last-shot').text(now.toLocaleString())
        $('#saved').text('')
        savePhoto(canvas.toDataURL('image/jpeg'));
      }
    }

    function singleShot() {
        snapshot();
        stopCamera();
    }

    function continuousShots() {
        $('.cap-button').hide();
        $('#cont-capture-stop').show();

        let current_min = 0;

        let min_time = 1
        let max_time = 10

        let capture_min = (Math.random() * (max_time - min_time)) + min_time
        capture_min = Math.round(capture_min)

        let capturing = setInterval(() => {
            current_min++;
            if (current_min === capture_min) {
                snapshot();
                capture_min = (Math.random() * (max_time - min_time)) + min_time
                capture_min = Math.round(capture_min)
                current_min = 0
            }
        }, 60000);

        $('#cont-capture-stop').off('click').one('click', () => {
            clearInterval(capturing);
            stopCamera();
        });

    }

    function startCamera() {
        navigator.mediaDevices.getUserMedia({video: true})
        .then(stream => {
          video.src = window.URL.createObjectURL(stream);
          localMediaStream = stream;
          $('.cap-button').show();
          $('#start-camera').hide();
          $('#cont-capture-stop').hide();
          $('#capture-info').show();
        })
        .catch(console.error);
    }

    function stopCamera() {
        video.pause();
        localMediaStream.getVideoTracks()[0].stop();
        $('.cap-button').hide();
        $('#start-camera').show();
    }

    app.setupImageCap = function(success_text, fail_text) {
        if (success_text) {
            post_success_text = success_text;
        }
        if (fail_text) {
            post_fail_text = fail_text
        }

        $('#capture-info').hide();
        $('.cap-button').hide();
        $('#start-camera').show();
        $('#start-camera').on('click', startCamera);
        $('#capture').on('click', singleShot);
        $('#cont-capture-start').on('click', continuousShots);
    }

})(app);