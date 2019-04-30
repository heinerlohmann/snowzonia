import os
import sys
import base64
import requests


def get_wave(fname):
    with open(fname) as infile:
        return base64.b64encode(infile.read())


endpoint = "https://snowboy.kitt.ai/api/v1/train/"

############# MODIFY THE FOLLOWING #############
token = "0414a99dc6a96237cfc8312519ab5a9d3152b324"
language = "dt"
age_group = "20_29"
gender = "M"
microphone = "PS3 Eye"
############### END OF MODIFY ##################

model_names = [
	"wakeword",
	"continue",
	"next",
	"previous",
	"play_track",
	"play_artist",
	"play_album",
	"play_playlist",
	"volume_up",
	"volume_down",
	"toggle_shuffle",
	"bluetooth_pairing",
	"enter_sleep_mode",
	"leave_sleep_mode"
]

data = None

def setdata(name):
    global data
    data = {
        "name": name,
       	"language": language,
        "age_group": age_group,
        "gender": gender,
        "microphone": microphone,
        "token": token,
        "voice_samples": [
            {"wave": get_wave("models" + dir  + "/" + name + "1.wav")},
            {"wave": get_wave("models" + dir  + "/" + name + "2.wav")},
            {"wave": get_wave("models" + dir  + "/" + name + "3.wav")}
        ]
    }

def sendrequest(name):
    global data
    out = 'models' + dir + '/' + name + ".pmdl"
    response = requests.post(endpoint, json=data)
    if response.ok:
        with open(out, "w") as outfile:
            outfile.write(response.content)
        print "Saved model to '%s'." % out
    else:
        print "Request failed."
        print response.text

if len(sys.argv) > 1:
	model_names = sys.argv[1:]

dir = raw_input("enter number of directory to use: models{1, 2} or any other name for a dir you have created (name = models[your input])")

for name in model_names:
        input = raw_input("SKIP sampling for the '" + name + "' model? [y] [Enter] (anything other than 'y' will start sampling for this model)").lower()
        if input != 'y':
		send_request = False
		while send_request == False:
			raw_input("press any key to record the first sample of the model: " + name)
			os.system('rec -r 16000 -c 1 -b 16 -e signed-integer models' + dir + '/' + name + '1.wav silence -l 1 0.1 1% 1 0.5 1% trim 0 3')
        		raw_input("press any key to record the second sample of the model: " + name)
        		os.system('rec -r 16000 -c 1 -b 16 -e signed-integer models' + dir + '/' + name + '2.wav silence -l 1 0.1 1% 1 0.5 1% trim 0 3')
			raw_input("press any key to record the third sample of the model: " + name)
        		os.system('rec -r 16000 -c 1 -b 16 -e signed-integer models' + dir + '/' + name + '3.wav silence -l 1 0.1 1% 1 0.5 1% trim 0 3')
                        os.system('aplay -D hw:0,0 models' + dir + '/' + name + '1.wav')
                        os.system('aplay -D hw:0,0 models' + dir + '/' + name + '2.wav')
                        os.system('aplay -D hw:0,0 models' + dir + '/' + name + '3.wav')
			input = raw_input("REDO this model? [y] [Enter] (anything other than 'y' will continue to the next model)").lower()
			if input == 'y':
   				send_request = False
			else:
   				send_request = True
		setdata(name)
		sendrequest(name)
print "all files were saved into models" + dir + " directory"
