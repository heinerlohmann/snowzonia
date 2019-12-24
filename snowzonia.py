#!/usr/bin/python

from snowboy import snowboydecoder
from r2d2 import R2D2
import snowzonia_player
import google_speech
import signal
import os
import sys
import traceback
import time
from thread import start_new_thread
from threading import Thread
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
	start_new_thread(r2d2.turn_head_randomly, (3, 0.3))
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
        os.path.join(model_path_1, "next.pmdl"),		#3
    	os.path.join(model_path_2, "next.pmdl")			#4
	]
else:
	wakeword_models = [
		os.path.join(model_path_1, "wakeword.pmdl"), 	#1
        os.path.join(model_path_1, "next.pmdl")	        #2
	]

command_models_1 = [
        os.path.join(model_path_1, "continue.pmdl"),		#1
        os.path.join(model_path_1, "next.pmdl"),			#2
        os.path.join(model_path_1, "previous.pmdl"),		#3
        os.path.join(model_path_1, "play_track.pmdl"),		#4
		os.path.join(model_path_1, "play_artist.pmdl"),		#5
        os.path.join(model_path_1, "play_album.pmdl"),		#6
        os.path.join(model_path_1, "play_playlist.pmdl"),	#7
        os.path.join(model_path_1, "volume_up.pmdl"),		#8
        os.path.join(model_path_1, "volume_down.pmdl"),		#9
		os.path.join(model_path_1, "enter_sleep_mode.pmdl")	#10
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
        os.path.join(model_path_2, "enter_sleep_mode.pmdl")     #10
	]

if multiple_users:
    leave_sleep_mode_models = [
        os.path.join(model_path_1, "leave_sleep_mode.pmdl"),	# 1
        os.path.join(model_path_2, "leave_sleep_mode.pmdl")		# 2
    ]
else:
    leave_sleep_mode_models = os.path.join(model_path_1, "leave_sleep_mode.pmdl")  # 1

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

# change to threading?
def start_command_timer():
	global command_timer
	if command_timer.is_alive():
	    command_timer.terminate()
	command_timer = Process(target=command_timeout_or_playback_started_from_elsewhere, args=(player_lock,))
	command_timer.start()

# initialize player
player = snowzonia_player.Player()

# initialize r2d2
r2d2 = R2D2()
class Button_Listener_Thread(Thread):
	def run(self):
		while True:
			print "listening to buttons..."
			if r2d2.but_next.is_pressed():
				print("button detected: next track")
				play_sound('next.wav', False)
				player_lock.acquire()
				player.next()
				player_lock.release()
			if r2d2.but_vol_up.is_pressed():
				print("button detected: volume up")
				player_lock.acquire()
				player.volume_up()
				player_lock.release()
			if r2d2.but_vol_down.is_pressed():
				print("button detected: volume down")
				player_lock.acquire()
				player.volume_down()
				player_lock.release()
			if r2d2.but_bluetooth.is_pressed():
				print "button detected: start bluetooth pairing"
				play_sound('startbluetoothpairing.wav', True)
				player_lock.acquire()
				player.start_bluetooth_pairing()
				player_lock.release()
			if r2d2.but_wifi.is_pressed():
				print "button detected: search for wifi"
				play_sound('startbluetoothpairing.wav', True)
			sleep(0.5)
button_listener = Button_Listener_Thread()
button_listener.start()
class Dance_Thread(Thread):
	while True:
		r2d2.random_dance()
dance = Dance_Thread()

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
		r2d2.led_blue1.on()
		if dance.is_alive():
			dance.terminate()
		r2d2.default_posture()
		start_new_thread(r2d2.turn_head_randomly, (1, 0.3))
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
		r2d2.led_blue1.on()
		if dance.is_alive():
			dance.terminate()
		r2d2.default_posture()
		start_new_thread(r2d2.turn_head_randomly, (1, 0.3))
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
	r2d2.led_blue2.on()
	start_new_thread(r2d2.turn_head_randomly, (1, 0.3))
	play_sound('continue.wav', False)
	player_lock.acquire()
	player.play()
	player_lock.release()
	return_to_wakeword_detection()

def next():
	print("command: next track")
	r2d2.led_blue2.on()
	start_new_thread(r2d2.turn_head_randomly, (1, 0.3))
	play_sound('next.wav', False)
    player_lock.acquire()
    player.next()
    player_lock.release()
    return_to_wakeword_detection()

def previous():
    print("command: previous track")
	r2d2.led_blue2.on()
	start_new_thread(r2d2.turn_head_randomly, (1, 0.3))
    play_sound('previous.wav', False)
    player_lock.acquire()
    player.previous()
    player_lock.release()
    return_to_wakeword_detection()

def play_track():
	print("command: play track x")
	r2d2.led_blue2.on()
	name = gcloud_query()
	print("gspeech understood: " + name)
	player_lock.acquire()
	player.play_track(name)
	player_lock.release()
	return_to_wakeword_detection()

def play_artist():
    print("command: play artist x")
	r2d2.led_blue2.on()
    name = gcloud_query()
    print("gspeech understood: " + name)
    player_lock.acquire()
    player.play_artist(name)
    player_lock.release()
    return_to_wakeword_detection()

def play_album():
    print("command: play album x")
	r2d2.led_blue2.on()
    name = gcloud_query()
    print("gspeech understood: " + name)
    player_lock.acquire()
    player.play_album(name)
    player_lock.release()
    return_to_wakeword_detection()

def play_playlist():
	print("command: play playlist x")
	r2d2.led_blue2.on()
	name = gcloud_query()
	print("gspeech understood: " + name)
	player_lock.acquire()
	player.play_playlist(name)
	player_lock.release()
	return_to_wakeword_detection()

def volume_up():
	print("command: volume up")
	r2d2.led_blue2.on()
	player_lock.acquire()
	player.volume_up()
	player_lock.release()
	play_sound('volumeup.wav', False)
	r2d2.led_blue2.off()

def volume_down():
	print("command: volume down")
	r2d2.led_blue2.on()
	player_lock.acquire()
	player.volume_down()
	player_lock.release()
	play_sound('volumedown.wav', False)
	r2d2.led_blue2.off()

def enter_sleep_mode():
	print("command: enter sleep mode")
	r2d2.led_blue2.on()
	start_new_thread(r2d2.sad_posture, (0.5))
	play_sound('entersleepmode.wav', True)
	r2d2.led_blue1.off()
	r2d2.led_blue2.off()
	start_sleep_mode_detection()

def dance():
	print("command: dance")
	r2d2.led_blue2.on()
	play_sound('continue.wav', False)
	player_lock.acquire()
	player.play()
	player_lock.release()
	dance.start()
	return_to_wakeword_detection()

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
	enter_sleep_mode
]

was_sleeping = False

def leave_sleep_mode_1():
	global was_sleeping
	global sleep_mode
	global user
	was_sleeping = True
	sleep_mode = False
	user = 1
	start_new_thread(r2d2.default_posture())
	play_sound('leavesleepmode.wav', True)
	print("waking up - starting command detection for user 1")

def leave_sleep_mode_2():
    global was_sleeping
    global sleep_mode
    global user
    was_sleeping = True
    sleep_mode = False
    user = 2
	start_new_thread(r2d2.default_posture())
    play_sound('leavesleepmode.wav', True)
    print("waking up- starting command detection for user 2")

if multiple_users:
	leave_sleep_mode = [leave_sleep_mode_1, leave_sleep_mode_2]
else:
	leave_sleep_mode = leave_sleep_mode_1

# change to threading, play at 100%?
def play_sound(file, as_process):
    try:
        if user == 1:
            if as_process:
				start_new_thread(os.system('aplay -q ' + os.path.join(SOUNDS_PATH_1, file))
                #Process(target=os.system('aplay -q ' + os.path.join(SOUNDS_PATH_1, file))).start()
            else:
                os.system('aplay -q ' + os.path.join(SOUNDS_PATH_1, file))
        elif user == 2:
            if as_process:
				start_new_thread(os.system('aplay -q ' + os.path.join(SOUNDS_PATH_2, file))
                #Process(target=os.system('aplay -q ' + os.path.join(SOUNDS_PATH_2, file))).start()
            else:
                os.system('aplay -q ' + os.path.join(SOUNDS_PATH_2, file))
    except:
        e = sys.exc_info()
        print(e[0])
        print(e[1])
        traceback.print_tb(e[2])


# interrupt callbacks of detectors
ignore_commands = True
sleep_mode = False
interrupted = False

def interrupt_callback():	# is called repeatedly by wakeword_detector while it is running
	return False

def interrupt_callback_commands():       # is called repeatedly by command_detector while it is running
	global ignore_commands
	if command_timer.is_alive() == False:
		ignore_commands = True
	return ignore_commands

def interrupt_callback_sleep_mode():
	if sleep_mode:
		return False
	else:
		return True

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
	if was_sleeping:
		return_from_sleep_mode()

def start_command_detection_2():
	global ignore_commands
	print("starting command detection for user 2")
	ignore_commands = False
	start_command_timer()
	commands_detector_2.ring_buffer.get() #clear audio buffer
	commands_detector_2.start(detected_callback=commands,
        interrupt_check=interrupt_callback_commands,
        sleep_time=0.03)
	if was_sleeping:
            return_from_sleep_mode()

def return_from_sleep_mode():
	global was_sleeping
	was_sleeping = False
	player_lock.acquire()
	player.pause()
	player_lock.release()
	if user == 1:
            start_command_detection_1()
	if user == 2:
            start_command_detection_2()

def start_sleep_mode_detection():
	global sleep_mode
	print("entering detection for leave-sleepmode-command")
	player_lock.acquire()
	if command_timer.is_alive():
            command_timer.terminate()
	player_lock.release()
	sleep_mode = True
	sleep_mode_detector.ring_buffer.get() #clear audio buffer
	sleep_mode_detector.start(detected_callback=leave_sleep_mode,
        interrupt_check=interrupt_callback_sleep_mode,
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
	r2d2.led_blue1.off()
	r2d2.led_blue2.off()

commands_detector_1 = snowboydecoder.HotwordDetector(command_models_1, sensitivity=0.4, audio_gain=1)

if multiple_users:
	commands_detector_2 = snowboydecoder.HotwordDetector(command_models_2, sensitivity=0.4, audio_gain=1)

sleep_mode_detector = snowboydecoder.HotwordDetector(leave_sleep_mode_models, sensitivity=0.4, audio_gain=1)

wakeword_detector = snowboydecoder.HotwordDetector(wakeword_models, sensitivity=0.4, audio_gain=1)
play_sound('leavesleepmode.wav', False)
wakeword_detector.start(detected_callback=wakewords,
    interrupt_check=interrupt_callback,
    sleep_time=0.03)

