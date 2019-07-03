#!/usr/bin/python

from snowboy import snowboydecoder
import snowzonia_player
import google_speech
import signal
import os
import sys
import traceback
import time
from multiprocessing import Process, Lock, Queue

PATH = os.path.dirname(os.path.abspath(__file__))
SOUNDS_PATH_1 = os.path.join(PATH, "sounds1")
SOUNDS_PATH_2 = os.path.join(PATH, "sounds2")

# seting up gcloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(PATH, "gcloudcreds.json")
def gcloud_query():
	global ignore_commands
	ignore_commands = True
	play_sound('startrecording.wav', False)
	os.system('rec -r 16000 -c 1 -b 16 -e signed-integer ' + os.path.join(PATH, "query.wav") + ' silence -l 1 0.1 1% 1 0.5 1% trim 0 5')
	play_sound('searching.wav', True)
	text = google_speech.send_gcloud_query(os.path.join(PATH, "query.wav"))
	return text

# models to use:
multiple_users = False
model_path_1 = os.path.join(PATH, "models1")

if multiple_users:
	model_path_2 = os.path.join(PATH, "models2")
	wakeword_models = [
			os.path.join(model_path_1, "wakeword.pmdl"),	#1
			os.path.join(model_path_2, "wakeword.pmdl"),	#2
                        os.path.join(model_path_1, "next.pmdl"),	#3
                        os.path.join(model_path_2, "next.pmdl")		#4
			]
else:
	wakeword_models = [
			os.path.join(model_path_1, "wakeword.pmdl"), 	#1
                        os.path.join(model_path_1, "next.pmdl")	        #2
			]

command_models_1 = [
        os.path.join(model_path_1, "continue.pmdl"),		#1
        os.path.join(model_path_1, "next.pmdl"),		#2
        os.path.join(model_path_1, "previous.pmdl"),		#3
        os.path.join(model_path_1, "play_track.pmdl"),		#4
	os.path.join(model_path_1, "play_artist.pmdl"),		#5
        os.path.join(model_path_1, "play_album.pmdl"),		#6
        os.path.join(model_path_1, "play_playlist.pmdl"),	#7
        os.path.join(model_path_1, "volume_up.pmdl"),		#8
        os.path.join(model_path_1, "volume_down.pmdl"),		#9
        os.path.join(model_path_1, "toggle_shuffle.pmdl"),	#10
        os.path.join(model_path_1, "bluetooth_pairing.pmdl"),	#11
	os.path.join(model_path_1, "enter_sleep_mode.pmdl")	#12
]
if multiple_users:
	command_models_2 = [
        	os.path.join(model_path_2, "continue.pmdl"),            #1
        	os.path.join(model_path_2, "next.pmdl"),                #2
        	os.path.join(model_path_2, "previous.pmdl"),            #3
        	os.path.join(model_path_2, "play_track.pmdl"),          #4
	        os.path.join(model_path_2, "play_artist.pmdl"),         #5
        	os.path.join(model_path_2, "play_album.pmdl"),          #6
        	os.path.join(model_path_2, "play_playlist.pmdl"),       #7
        	os.path.join(model_path_2, "volume_up.pmdl"),           #8
        	os.path.join(model_path_2, "volume_down.pmdl"),         #9
        	os.path.join(model_path_2, "toggle_shuffle.pmdl"),      #10
        	os.path.join(model_path_2, "bluetooth_pairing.pmdl"),   #11
	        os.path.join(model_path_2, "enter_sleep_mode.pmdl")     #12
]

# command timeout -> back to wakeword detection
# note that terminating the command_timer without acquiring the player_lock first may cause a deadlock
# the player_lock is needed to avoid two dbus calls at the same time, because the responses could get mixed up
def command_timeout_or_playback_started_from_elsewhere(player_lock):
	start_time = time.time()
	first_sound = start_time + 120
	second_sound = start_time + 240
	timeout = start_time + 360
	first_sound_played = False
	second_sound_played = False
	playing = False
	while time.time() < timeout and playing == False:
		if time.time() > first_sound and first_sound_played == False:
			play_sound('commandtimer1.wav', True)
			first_sound_played = True
		if time.time() > second_sound and second_sound_played == False:
                        play_sound('commandtimer2.wav', True)
                        second_sound_played = True
		time.sleep(1)
		player_lock.acquire()
		playing = player.is_playing()
		player_lock.release()
	if playing == False:
		print("command timeout -> going back to wakeword detection")
	else:
        	print("playback started -> going back to wakeword detection")

player_lock = Lock()
command_timer = Process(target=command_timeout_or_playback_started_from_elsewhere, args=(player_lock,))

def start_command_timer():
	global command_timer
	if command_timer.is_alive():
		command_timer.terminate()
	command_timer = Process(target=command_timeout_or_playback_started_from_elsewhere, args=(player_lock,))
	command_timer.start()

# initialize player
player = snowzonia_player.Player()

# exception handler
def handle_exception():
	global ignore_commands
	e = sys.exc_info()
	print(e[0])
	print(e[1])
	traceback.print_tb(e[2])
	lock_free = player_lock.acquire(False)
	if lock_free == False:
		player_lock.release()
		player_lock.acquire()
	ignore_commands = True
	if command_timer.is_alive():
                command_timer.terminate()
	player_lock.release()
	print("going back to wakeword detection after an exception occured")
	play_sound('exception.wav', False)

# callbacks
user = 1

def wakeword_1():
	global user
	global ignore_commands
	try:
		user = 1
		player_lock.acquire()
		player.pause()
		player_lock.release()
		play_sound('wakeword.wav', True)
		start_command_detection_1()
	except:
		handle_exception()

def wakeword_2():
	global user
	global ignore_commands
	try:
		user = 2
		player_lock.acquire()
		player.pause()
		player_lock.release()
		play_sound('wakeword.wav', True)
		start_command_detection_2()
	except:
		handle_exception()

def next_from_wakeword_detection():
	try:
		print("command: next track")
		play_sound('next.wav', False)
		player_lock.acquire()
		player.next()
		player_lock.release()
	except:
                handle_exception()

if multiple_users:
        wakewords = [wakeword_1, wakeword_2, next_from_wakeword_detection, next_from_wakeword_detection]
else:
        wakewords = [wakeword_1, next_from_wakeword_detection]

def continuepb():
	print("command: continue playback")
	play_sound('continue.wav', False)
	player_lock.acquire()
	player.play()
	player_lock.release()
	return_to_wakeword_detection()

def next():
        print("command: next track")
        play_sound('next.wav', False)
        player_lock.acquire()
        player.next()
        player_lock.release()
        return_to_wakeword_detection()

def previous():
        print("command: previous track")
        play_sound('previous.wav', False)
        player_lock.acquire()
        player.previous()
        player_lock.release()
        return_to_wakeword_detection()

def play_track():
	print("command: play track x")
	name = gcloud_query()
	print("gspeech understood: " + name)
	player_lock.acquire()
	player.play_track(name)
	player_lock.release()
	return_to_wakeword_detection()

def play_artist():
        print("command: play artist x")
        name = gcloud_query()
        print("gspeech understood: " + name)
        player_lock.acquire()
        player.play_artist(name)
        player_lock.release()
        return_to_wakeword_detection()

def play_album():
        print("command: play album x")
        name = gcloud_query()
        print("gspeech understood: " + name)
        player_lock.acquire()
        player.play_album(name)
        player_lock.release()
        return_to_wakeword_detection()

def play_playlist():
	print("command: play playlist x")
	name = gcloud_query()
	print("gspeech understood: " + name)
	player_lock.acquire()
	player.play_playlist(name)
	player_lock.release()
	return_to_wakeword_detection()

def volume_up():
	print("command: volume up")
	player_lock.acquire()
	player.volume_up()
	player_lock.release()
	play_sound('volumeup.wav', False)

def volume_down():
	print("command: volume down")
	player_lock.acquire()
	player.volume_down()
	player_lock.release()
	play_sound('volumedown.wav', False)

def toggle_shuffle():
	print("command: toggle shuffle")
	player_lock.acquire()
	shuffle_on = player.toggle_shuffle()
	player_lock.release()
	if shuffle_on:
		play_sound('shuffleON.wav', False)
	else:
		play_sound('shuffleOFF.wav', False)

def bluetooth_pairing():
	print("command: start bluetooth pairing")
	play_sound('startbluetoothpairing.wav', True)
	player_lock.acquire()
	player.start_bluetooth_pairing()
	player_lock.release()

def enter_sleep_mode():
	print("command: enter sleep mode")
	play_sound('entersleepmode.wav', True)
	subprocess.call(['shutdown', '-h', 'now'], shell=False)
	
commands = [
	continuepb,
	next,
	previous,
	play_track,
	play_artist,
	play_album,
	play_playlist,
	volume_up,
	volume_down,
	toggle_shuffle,
	bluetooth_pairing,
	enter_sleep_mode
]

def play_sound(file, as_process):
	try:
		if user == 1:
			if as_process:
				Process(target=os.system('aplay -q ' + os.path.join(SOUNDS_PATH_1, file))).start()
			else:
				os.system('aplay -q ' + os.path.join(SOUNDS_PATH_1, file))
		elif user == 2:
                	if as_process:
                                Process(target=os.system('aplay -q ' + os.path.join(SOUNDS_PATH_2, file))).start()
                	else:
                        	os.system('aplay -q ' + os.path.join(SOUNDS_PATH_2, file))
	except:
		e = sys.exc_info()
		print(e[0])
		print(e[1])
		traceback.print_tb(e[2])


# interrupt callbacks of detectors
ignore_commands = True
interrupted = False

def interrupt_callback():	# is called repeatedly by wakeword_detector while it is running
	return False

def interrupt_callback_commands():       # is called repeatedly by command_detector while it is running
	global ignore_commands
	if command_timer.is_alive() == False:
		ignore_commands = True
	return ignore_commands

# detection
def start_command_detection_1():
	global ignore_commands
	print("starting command detection for user 1")
	ignore_commands = False
	start_command_timer()
	commands_detector_1.ring_buffer.get() #clear audio buffer
	commands_detector_1.start(detected_callback=commands,
               				interrupt_check=interrupt_callback_commands,
               				sleep_time=0.03)

def start_command_detection_2():
	global ignore_commands
	print("starting command detection for user 2")
	ignore_commands = False
	start_command_timer()
	commands_detector_2.ring_buffer.get() #clear audio buffer
	commands_detector_2.start(detected_callback=commands,
                                        interrupt_check=interrupt_callback_commands,
                                        sleep_time=0.03)

def return_to_wakeword_detection():
	global ignore_commands
	ignore_commands = True
	player_lock.acquire()
	if command_timer.is_alive():
		command_timer.terminate()
	player_lock.release()
	wakeword_detector.ring_buffer.get() #clear audio buffer
	print("returning to wakeword detection")

commands_detector_1 = snowboydecoder.HotwordDetector(command_models_1, sensitivity=0.4, audio_gain=1)

if multiple_users:
	commands_detector_2 = snowboydecoder.HotwordDetector(command_models_2, sensitivity=0.4, audio_gain=1)

wakeword_detector = snowboydecoder.HotwordDetector(wakeword_models, sensitivity=0.4, audio_gain=1)
play_sound('leavesleepmode.wav', False)
wakeword_detector.start(detected_callback=wakewords,
        	       	interrupt_check=interrupt_callback,
               		sleep_time=0.03)
