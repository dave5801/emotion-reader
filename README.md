# Emotion Reader

## What is Emotion Reader?

## Get Started

## Influences and Attributions

Below are the people and libraries we used to make this project possible.

### People
-----------

### Libraries
--------------
#### Microsoft API's
Microsoft has some pretty amazing API's in general that a user can hit, we were lucky enough to find two from Microsoft to use for our project.
##### Face API
* Face API can detect up to 64 human faces then can be handle with the use of bytes or url.
* Face API can compare 2 different faces and determine if they are the same person or not. This is what we used for Authentication and Authorization for our Face Login feature.
* Face API has many more features. Check them out here [Face API Documenation](https://docs.microsoft.com/en-us/azure/cognitive-services/face/overview).
##### Emotion API
* Emotion API takes in an expression as an input, returns a bounded box using Face API, and returns a JSON object with 8 emotions.

Example of a single face.
-------------------------- 
```
JSON:
 [
  {
    "faceRectangle": {
      "top": 114,
      "left": 212,
      "width": 65,
      "height": 65
    },
    "scores": {
      "anger": 1.0570484E-08,
      "contempt": 1.52679547E-09,
      "disgust": 1.60232943E-07,
      "fear": 6.00660363E-12,
      "happiness": 0.9999998,
      "neutral": 9.449728E-09,
      "sadness": 1.23025981E-08,
      "surprise": 9.91396E-10
    }
  }
 ]
 ```

Check out Emotion API and [Emotion API Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/emotion/home).
#### Spotify
We used what Spotify calls ["The Play Button"](https://developer.spotify.com/technologies/widgets/spotify-play-button/). This is a widget where you can copy and paste in a playlist URI and spits out an iframe for you to use with your site.

Example of iframe:
```
<iframe src="https://open.spotify.com/embed?uri=spotify:user:spotify:playlist:3rgsDhGHZxZ9sB9DQWQfuf" width="300" height="380" frameborder="0" allowtransparency="true"></iframe>
```

With the use of the iframe you can adjust the height, width, and border for the overall look.
## License
Emotion Reader is offered under the MIT license and shown in the LICENSE file.`
## Authors
* [David Franklin](https://github.com/dave5801)
* [Megan Flood](https://github.com/musflood)
* [Zach Taylor](https://github.com/ztaylor2)
* [Michael Shinners](https://github.com/mshinners)
* [Jacob Carstens](https://github.com/Loaye)