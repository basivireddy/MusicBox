# What is Music Box?

Music Box is an application that let's you upload, store, and play all of your music from the cloud. You can now manage and listen to your music from any device, anywhere in the world.

[**Docker**](#docker) | [**Installation Instructions**](#installation) 
------

## ScreenShot: ##

![ScreenShot](https://raw.githubusercontent.com/basivireddy/MusicBox/master/MusicBox.PNG)

-------

## Docker

```
docker run -it -d --name musicbox basivireddy/musicbox:latest

```
## Installation 

### Create virtual environment and activate(optional)
```
    virtualenv ENV
    source ENV/bin/activate
```

### Download MusicBox
```
    git clone https://github.com/basivireddy/MusicBox.git
```

### Install  required packages
```
   cd MusicBox
   pip install -r requirements.txt
```
### Run the server
```
   python manage.py runserver 0.0.0.0:8000
```
then browse ***http://your_server_ip:8000/music/***
