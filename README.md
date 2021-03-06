# Emotion Reader
[![Build Status](https://travis-ci.org/dave5801/emotion-reader.svg?branch=master)](https://travis-ci.org/dave5801/emotion-reader)
[![Coverage Status](https://coveralls.io/repos/github/dave5801/emotion-reader/badge.svg?branch=master)](https://coveralls.io/github/dave5801/emotion-reader?branch=master)

## What is Emotion Reader?
Emotion Reader is an application that takes photos and analyzes your face and outputs an emotion.
## Get Started
---------------
Clone this repository to your local machine.
```
$ git clone https://github.com/dave5801/emotion-reader.git
```
Once downloaded, change directory into the emotionreader directory.
```
$ cd emotion-reader
```
Begin a new virtual environment with Python 3 and activate it.
```
emotion-reader $ python3 -m venv ENV

emotion-reader $ source ENV/bin/activate
```
Install the application requirements with [`pip`](https://pip.pypa.io/en/stable/installing/).
```
(ENV) emotion-reader $ pip install -r requirements.txt
```
Create a [Postgres](https://wiki.postgresql.org/wiki/Detailed_installation_guides) database for use with this application.
```
(ENV) emotion-reader $ createdb emotionreader
```

Export environmental variables pointing to the location of database, your username, hashed password, and secret.

```
(ENV) emotion-reader $ export SECRET_KEY='secret'

(ENV) emotion-reader $ export DB_NAME='emotionreader'

(ENV) emotion-reader $ export DB_USER='(your postgresql username)'

(ENV) emotion-reader $ export DB_PASS='(your postgresql password)'

(ENV) emotion-reader $ export DB_HOST='localhost'

(ENV) emotion-reader $ export DEBUG='True'
```

Then initialize the database with the `migrate` command from `manage.py`

```
(ENV) emotion-reader $ python emotionreader/manage.py migrate
```
Once the package is installed and the database is created, start the server with the `runserver` command from `manage.py`
```
(ENV) emotion-reader $ python emotionreader/manage.py runserver
```
Application is served on http://localhost:8000

### Testing
You can test this application by first exporting an environmental variable pointing to the location of a testing database, then running the `test` command from `manage.py`.

```
(ENV) emotion-reader $ export

TEST_DB='test_emotionreader'

(ENV) emotion-reader $ python

emotionreader/manage.py test emotionreader
```


## Influences and Attributions
--------------------------------

Below are the libraries and technologies we used to make this project possible.
### Libraries
--------------

### Template
-------------

#### [Django(1.11)](https://docs.djangoproject.com/en/1.11/)

Get started with Django

```
pip install django==1.11
```

Django has three layers.
* Model Layer
    * An abstraction layer where you can create your models

    ```
    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
    ```

* View Layer
    * Where request and responses get handled.

    ```
    from django.conf.urls import url

    from . import views

    urlpatterns = [
        url(r'^articles/2003/$', views.special_case_2003),
        url(r'^articles/([0-9]{4})/$', views.year_archive),
        url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
        url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
    ]
    ```

* Template Layer
    * How the information being passed gets served to the front end.

    ```
        TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                # ... some options here ...
            },
        },
    ]
    ```

To dive deeper into the documentations for a more in depth idea of how we set everything up. [Click Here](https://docs.djangoproject.com/en/1.11/)
### API
--------
#### Microsoft API's
Microsoft has some pretty amazing API's in general that a user can hit, we were lucky enough to find two from Microsoft to use for our project.
##### Face API
* Face API can detect up to 64 human faces then can be handle with the use of bytes or url.
* Face API can compare 2 different faces and determine if they are the same person or not. This is what we used for Authentication and Authorization for our Face Login feature.
* Face API has many more features. Check out the Face API and [Face API Documenation](https://docs.microsoft.com/en-us/azure/cognitive-services/face/overview).
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

### Services(Amazon)
--------------------

### [Amazon(AWS)](https://aws.amazon.com/documentation/)
#### [Amazon RDS](https://aws.amazon.com/documentation/rds/)
Relational Database Service
##### What is a Relational Database?
A relational database is a collection of items that hold data. These items have pre-defined relationships before they are put into a table with columns and rows to sort. The data holds information that relates to objects that are being represented. Each row and column has a unique identifier. We use this identifier to talk between pieces.

* Amazon's version of a relational database in the cloud. 
* Simplicity and scalablity is always in mind when it comes to building out these apps. RDS gives us that.
* We are able to have a built out front-end so we can manage and handle out databases when we need to but don't have to worry about maintaining them. They are automated.
#### [Amazon S3](https://aws.amazon.com/documentation/s3/)
Simple Storage Service
* S3 is a simple way to store data in the cloud and have the ability to access it any place and any time in the world.
* We created a bucket(storage) and received a key that routes to that bucket. When ever we push data, it uses this key and pushes it to the bucket.
* Using S3 allows our app to be smaller, compact, and more efficient.
#### [Amazon EC2](https://aws.amazon.com/documentation/ec2/)
Elastic Compute Cloud
* EC2 is a simple way to compute data in the cloud.
* EC2 is secure and resizeable. 
* Similar to S3 which setting up. Create an instance, set parameters, and get a key. Use that key to route information there, process it, and then your parameters push it somewhere else.
#### [Amazon Route 53](https://aws.amazon.com/documentation/route53/)
Route 53
* Cloud Domain Name System(DNS).
* We are routing our EC2 instance to our domain.

### Design
-----------
#### [Chart.js](http://www.chartjs.org/docs/latest/)
* Chart.js passes in data and organizes and displays the information int a chart. 
* These charts can vary in design and interaction.
#### [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
* Bootstrap is a design templating service. 
* Through the use of a design library with [jQuery](https://jquery.com/) and [SCSS](http://sass-lang.com/) as major players, we have an amazing design tool where we can plug and play chunks of code to have a polished front end.
* Our specific bootstrap that we used was [Light Bootsrap](https://www.creative-tim.com/product/light-bootstrap-dashboard).
### Widgets
------------
#### Spotify
We used what Spotify calls ["The Play Button"](https://developer.spotify.com/technologies/widgets/spotify-play-button/). This is a widget where you can copy and paste in a playlist URI and spits out an iframe for you to use with your site.

Example of iframe:
```
<iframe src="https://open.spotify.com/embed?uri=spotify:user:spotify:playlist:3rgsDhGHZxZ9sB9DQWQfuf" width="300" height="380" frameborder="0" allowtransparency="true"></iframe>
```

With the use of the iframe you can adjust the height, width, and border for the overall look.

### Automation
---------------
#### [Ansible](https://www.ansible.com/)
* Running Ansible Playbook
    ```
    ansible -playbook -i hosts playbooks/emotion_playbook.yml
    ```

* Ansible automates tasks. Some of these tasks are:
    * Installs all the applications
    * Clones repo to EC2 instance
    * Creates all necessary files needed for the app
## License
Emotion Reader is offered under the MIT license and shown in the LICENSE file.`
## Authors
* [David Franklin](https://github.com/dave5801)
* [Megan Flood](https://github.com/musflood)
* [Zach Taylor](https://github.com/ztaylor2)
* [Michael Shinners](https://github.com/mshinners)
* [Jacob Carstens](https://github.com/Loaye)