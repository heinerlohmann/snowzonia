# Snowzonia

Snowzonia is a voice interface for playback control, it uses [Snowboy Hotword Detection](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) to detect commands and plays music (or other audio) from [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) or any connected bluetooth device, that supports [A2DP](https://de.wikipedia.org/wiki/A2DP) and [AVRCP](https://de.wikipedia.org/wiki/AVRCP) (e.g. iOS or Android devices).

Simple commands are interpreted on device by Snowboy, but search queries like a track, artist etc. are transcriped by [Google Speech](https://cloud.google.com/speech-to-text/), so you will need a gcloud-account for this functionality. There are other speech to text solutions, but considering the diversity and randomness in names of artists and songs, I dont think most of them are suitable in this context. But if you only want to play a small, finite amount of playlists with names that don't change you could make it work with Snowboy alone and some changes in the code.

Please note, that the project is still lacking most of the documentation, so be prepared to get frustrated or wait until I find the time to write it.

## Getting Started
coming soon
### Prerequisites
coming soon
### Installing
coming soon

## Contributing
I did this project to learn more about Python and Linux, because I was new to both. I basically wrote the whole code with the nano editor on a Raspberry Pi. There are probably many things I could have done better in many ways, so feel free to contribute to the project or lecture me on what's wrong with it. ;)

## Author
Heiner Lohmann

## Acknowledgments
Most of the credits for this project should go to [Snowboy Hotword Detection](https://github.com/Kitt-AI/snowboy#snowboy-hotword-detection) and [Tizonia](https://github.com/tizonia/tizonia-openmax-il#the-tizonia-project) since Snowzonia is basically just a middleman between them.
