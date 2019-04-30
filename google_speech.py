#!/usr/bin/python

import io
import unicodedata

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech

def send_gcloud_query(file_name):

	# Instantiates a client
	client = speech.SpeechClient()

	# Loads the audio into memory
	with io.open(file_name, 'rb') as audio_file:
    		content = audio_file.read()
    		audio = speech.types.RecognitionAudio(content=content)

	config = speech.types.RecognitionConfig(
    		encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    		sample_rate_hertz=16000,
    		language_code='en-US',
		alternative_language_codes=['de-De'])

	# Detects speech in the audio file
	response = client.recognize(config, audio)

	text = response.results[0].alternatives[0].transcript
	text = unicodedata.normalize('NFKD', text)
	text = text.encode('ascii','ignore')

	return text
