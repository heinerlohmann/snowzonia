# Snowzonia

Snowzonia is a voice interface for playback control, it uses [Snowboy Hotword Detection](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) to detect commands and plays music (or other audio) from [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) or any connected bluetooth device, that supports [A2DP](https://de.wikipedia.org/wiki/A2DP) and [AVRCP](https://de.wikipedia.org/wiki/AVRCP) (e.g. iOS or Android devices).

Simple commands are interpreted on device by Snowboy, but search queries like a track, artist etc. are transcriped by [Google Speech](https://cloud.google.com/speech-to-text/), so you will need a gcloud-account for this functionality. There are other speech to text solutions, but considering the diversity and randomness in names of artists and songs, I dont think most of them are suitable in this context. But if you only want to play a small, finite amount of playlists with names that don't change you could make it work with Snowboy alone and some changes in the code.

Please note, that the project is still lacking most of the documentation, so be prepared to get frustrated or wait until I find the time to write it.

## Getting Started
This guide will help you to set up Snowzonia on a Linux device. It should work on most Debian based Linux machines, but I have only tested it on Raspberry Pi with Raspbian Stretch Desktop.

Warning: Do yourself a favour and do not use Raspbian Stretch Lite with Snowzonia, even though you might run your device headless. Snowzonia communicates with [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) and [BlueZ](http://www.bluez.org/) (Linux Bluetooth stack) via [DBUS](https://www.freedesktop.org/wiki/Software/dbus/) which depends on X11 (window manager) which is not included in Raspbian Stretch Lite and also has its own dependencies. So save yourself a lot of time and just use Raspbian Stretch Desktop.

### Prerequisites
You will need to get [Snowboy](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) and an USB-microphone.
To get the USB-microphone working might be the hardest part of this.
Follow the [instructions](http://docs.kitt.ai/snowboy/) and download pre-packaged Snowboy binaries and their Python wrappers for your system to get Snowboy working. You won't need to train any models for Snowzonia yet. (since you may need 14 of them, I wrote a script for that)

If you only want a voice controlled bluetooth-speaker Snowboy is pretty much all you need and you can continue with the Installing-section.

If you want to listen to music (without a connected bluetooth-device) from streaming services (e.g. Spotify) you will need [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project).

Easy install for Tizonia:
(may take a long, long while on a raspberry)

    curl -kL https://goo.gl/Vu8qGR | bash
    
 After installing Tizonia check the location of its config file:
 
    tizonia --help config
Edit the config file and add your streaming service credentials.


If you want to tell Tizonia what exactly it should play you will need a sophisticated speech-to-text engine. By default Snowzonia will try to use [Google Speech](https://cloud.google.com/speech-to-text/), but you will need your own credentials and the python client library.

Get Google Speech:
(may take a while on a raspberry)

    pip install --upgrade google-cloud-speech

[PulseAudio](https://en.wikipedia.org/wiki/PulseAudio) is needed for Tizonia and A2DP, which also needs the PulseAudio bluetooth module.

    apt-get install pulseaudio pulseaudio-module-bluetooth

### Installing
Go to your home folder.
Clone the snowzonia repository:

    git clone https://github.com/heinerlohmann/snowzonia.git

Assuming you have downloaded [the pre-packaged Snowboy binaries and their Python wrappers for your system](http://docs.kitt.ai/snowboy/#downloads) and already extracted them, move them to the snowboy subdirectory in the snowzonia directory.

    mv <snowboy path, e.g. /home/pi/rpi-arm-raspbian-8.0-1.1.1>/* <snowzonia path, e.g. /home/pi/snowzonia>/snowboy

Edit the modify-section of train_snowboy.py and execute it to train your models.

    nano train_snowboy.py
    python trainsnowboy.py

In order to use Google Speech you have to save the json file with your credentials you got from google as "gcloudcreds.json" inside the snowzonia directory.

Test if everything works:

    python snowzonia.py

I included a systemd unit file, if you want to run snowzonia as a service.

## Contributing
I did this project to learn more about Python and Linux, because I was new to both. I basically wrote the whole code in the nano editor on a Raspberry Pi. There are probably many things I could have done better in many ways, so feel free to contribute to the project or lecture me on what's wrong with it. ;)

## Author
Heiner Lohmann

## Acknowledgments
Most of the credits for this project should go to [Snowboy Hotword Detection](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) and [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) since Snowzonia is basically just a middleman between them.
