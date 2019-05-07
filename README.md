# Snowzonia

Snowzonia is a voice interface for playback control, it uses [Snowboy Hotword Detection](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) to detect commands and plays music (or other audio) from [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) or any connected bluetooth device, that supports [A2DP](https://de.wikipedia.org/wiki/A2DP) and [AVRCP](https://de.wikipedia.org/wiki/AVRCP) (e.g. iOS or Android devices).

Simple commands are interpreted on device by Snowboy, but search queries like a track, artist etc. are transcriped by [Google Speech](https://cloud.google.com/speech-to-text/), so you will need a gcloud-account for this functionality. There are other speech to text solutions, but considering the diversity and randomness in names of artists and songs, I dont think most of them are suitable in this context. But if you only want to play a small, finite amount of playlists with names that don't change you could make it work with Snowboy alone and some changes in the code.

Please note, that the project is still lacking most of the documentation, so be prepared to get frustrated or wait until I find the time to write it.

## Getting Started
This guide will help you to set up Snowzonia on a Linux device. It should work on most Debian based Linux machines, but I have only tested it on Raspberry Pi with Raspbian Stretch Desktop.

Warning: Do yourself a favour and do not use Raspbian Stretch Lite with Snowzonia, even though you might run your device headless. Snowzonia communicates with [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) and [BlueZ](http://www.bluez.org/) (Linux Bluetooth stack) via [DBUS](https://www.freedesktop.org/wiki/Software/dbus/) which depends on X11 (window manager) which is not included in Raspbian Stretch Lite and also has its own dependencies. So save yourself a lot of time and just use Raspbian Stretch Desktop.

### Prerequisites
You will need to get [Snowboy](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) and an USB-microphone.
Follow the [instructions](http://docs.kitt.ai/snowboy/) to get everything working. You won't need to train any models for Snowzonia yet. (since you may need 14 of them, I wrote a script for that)

If you only want a voice controlled bluetooth-speaker Snowboy is pretty much all you need and you can continue with the Installing-section.

If you want to listen to music (without a connected bluetooth-device) from streaming services (e.g. Spotify) you will need [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project).
Easy install for Tizonia: (may take a long, long while on a raspberry)

    curl -kL https://goo.gl/Vu8qGR | bash

If you want to tell Tizonia what exactly it should play you will need a sophisticated speech-to-text engine. By default Snowzonia will try to use [Google Speech](https://cloud.google.com/speech-to-text/), but you will need your own credentials and the python client library.
Get Google Speech: (may take a while on a raspberry)

    pip install --upgrade google-cloud-speech

When you play music with your Pi you maybe use a HifiBerry, USB-soundcard or a similar product, because the onboard sound of the Pi is not that great. (although it is sufficient for some users)
If that is the case, you should consider using [PulseAudio](https://en.wikipedia.org/wiki/PulseAudio) to handle to different external sound cards (mic and soundcard). You will need it anyways for Tizonia.

    apt-get install pulseaudio


### Installing
coming soon

## Contributing
I did this project to learn more about Python and Linux, because I was new to both. I basically wrote the whole code in the nano editor on a Raspberry Pi. There are probably many things I could have done better in many ways, so feel free to contribute to the project or lecture me on what's wrong with it. ;)

## Author
Heiner Lohmann

## Acknowledgments
Most of the credits for this project should go to [Snowboy Hotword Detection](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) and [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) since Snowzonia is basically just a middleman between them.
