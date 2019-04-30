import dbus
import time
import os

def get_service_name():
	sessionbus = dbus.SessionBus()
	sessionbus_object = sessionbus.get_object("org.freedesktop.DBus", "/")
	sessionbus_names = sessionbus_object.ListNames(dbus_interface='org.freedesktop.DBus')
	for name in sessionbus_names:
		if 'tizonia' in name:
			return name
	return 'nothing'

def get_proxy_object():
        return dbus.SessionBus().get_object(get_service_name(), '/com/aratelia/tiz/tizonia')

def get_playback_interface():
        proxy = get_proxy_object()
        return dbus.Interface(proxy, dbus_interface='org.mpris.MediaPlayer2.Player')

def get_properties():
        proxy = get_proxy_object()
        return dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')

def get_volume():
	return get_properties().Get('org.mpris.MediaPlayer2.Player', 'Volume')

def set_volume(value):
	get_properties().Set('org.mpris.MediaPlayer2.Player', 'Volume', value)

def play():
        if status() == 'Paused':
		playback = get_playback_interface()
        	playback.Play()

def pause():
	if status() == 'Playing':
		playback = get_playback_interface()
	        playback.Pause()

def play_track(name):
	print 'tizonia will try to play track: ' + name
	if is_running():
		quit()
	os.system('tizonia -d --spotify-tracks "' + str(name) + '"')
	wait_until_playing()

def play_artist(name, shuffle):
        print 'tizonia will try to play artist: ' + name
        if is_running():
                quit()
        if shuffle == True:
                os.system('tizonia -d --spotify-artist "' + str(name) + '" --shuffle')
        else:
                os.system('tizonia -d --spotify-artist "' + str(name) + '"')
        wait_until_playing()

def play_album(name, shuffle):
        print 'tizonia will try to play album: ' + name
        if is_running():
		quit()
	if shuffle == True:
		os.system('tizonia -d --spotify-album "' + str(name) + '" --shuffle')
        else:
		os.system('tizonia -d --spotify-album "' + str(name) + '"')
        wait_until_playing()

def play_playlist(name, shuffle):
        print 'tizonia will try to play playlist: ' + name
        if is_running():
		quit()
        if shuffle == True:
                os.system('tizonia -d --spotify-playlist "' + str(name) + '" --shuffle')
        else:
		os.system('tizonia -d --spotify-playlist "' + str(name) + '"')
	wait_until_playing()

def next():
        playback = get_playback_interface()
	play()
        playback.Next()

def previous():
        playback = get_playback_interface()
        play()
        playback.Previous()

# sadly, this method has no effect on tizonia (yet?)
def shuffle():
	properties = get_properties()
	shuffle = properties.Get('org.mpris.MediaPlayer2.Player', 'Shuffle')
	if shuffle == False:
		properties.Set('org.mpris.MediaPlayer2.Player', 'Shuffle', True)
	else:
		properties.Set('org.mpris.MediaPlayer2.Player', 'Shuffle', False)

def status():
	if is_running():
        	return str(get_properties().Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus'))
	else:
		return 'not running'

def is_running():
	if get_service_name() == 'nothing':
		return False
	else:
		return True

def quit():
        proxy = get_proxy_object()
        interface = dbus.Interface(proxy, dbus_interface='org.mpris.MediaPlayer2')
	interface.Quit()

def wait_until_playing():
        timeout = time.time() + 10
	while status() != 'Playing' and time.time() < timeout:
                time.sleep(0.25)

