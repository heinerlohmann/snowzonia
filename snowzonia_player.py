import os
import tizonia_interface as tizonia
import bluez_interface as bluez

class Player():

	def __init__(self):
		os.system('amixer -q set Master 50%')
		self.volume = 0.5
		self.last_played = ['playlist', 'Classic Rock'] #default
		self.shuffle = True
		self.shuffle_changed = False

	# universal methods

	def status(self):
		status = { 'tizonia' : tizonia.status(), 'bluez' : bluez.status() }
		return status

	def is_playing(self):
		if bluez.status() == 'playing':
			return True
		if tizonia.status() == 'Playing':
			return True
		return False

	def volume_up(self):
		if self.volume < 1.0:
			self.volume = self.volume + 0.1
		os.system('amixer -q set Master ' + str(int(self.volume*100)) + '%')

	def volume_down(self):
		if self.volume > 0.0:
                        self.volume = self.volume - 0.1
		os.system('amixer -q set Master ' + str(int(self.volume*100)) + '%')

	def play(self):
		if bluez.is_running():
			bluez.play()
		elif tizonia.is_running() and self.shuffle_changed == False:
			tizonia.play()
			tizonia.set_volume(self.volume)
		else:
			if self.last_played[0] == 'track':
				self.play_track(self.last_played[1])
			elif self.last_played[0] == 'artist':
                                self.play_artist(self.last_played[1])
			elif self.last_played[0] == 'album':
                                self.play_album(self.last_played[1])
			elif self.last_played[0] == 'playlist':
                                self.play_playlist(self.last_played[1])
		if self.shuffle_changed:
			self.shuffle_changed = False

	def pause(self):
		if bluez.is_running():
                        bluez.pause()
		if tizonia.is_running():
                        tizonia.pause()

	def next(self):
		if bluez.is_running():
                        bluez.next()
		elif tizonia.is_running():
			tizonia.next()
			tizonia.set_volume(self.volume)

	def previous(self):
                if bluez.is_running():
                        bluez.previous()
                elif tizonia.is_running():
                        tizonia.previous()
                        tizonia.set_volume(self.volume)

	# tizonia-only methods

	def play_track(self, name):
		tizonia.play_track(name)
		self.last_played = ['track', name]
		self.tizonia_is_active = True
		tizonia.set_volume(self.volume)
		bluez.disconnect_device()

	def play_artist(self, name):
                tizonia.play_artist(name, self.shuffle)
                self.last_played = ['artist', name]
                self.tizonia_is_active = True
                tizonia.set_volume(self.volume)
                bluez.disconnect_device()

	def play_album(self, name):
		tizonia.play_album(name, self.shuffle)
		self.last_played = ['album', name]
		self.tizonia_is_active = True
		tizonia.set_volume(self.volume)
		bluez.disconnect_device()

	def play_playlist(self, name):
		tizonia.play_playlist(name, self.shuffle)
		self.last_played = ['playlist', name]
		self.tizonia_is_active = True
		tizonia.set_volume(self.volume)
		bluez.disconnect_device()

	def toggle_shuffle(self):
		if self.shuffle == False:
			self.shuffle = True
			print('shuffle now on')
		else:
			self.shuffle = False
			print('shuffle now off')
		self.shuffle_changed = True
		return self.shuffle

	# bluez-only methods

	def start_bluetooth_pairing(self):
		print('starting bluetooth pairing...')
		bluez.start_pairing()
		print('pairing ended')
