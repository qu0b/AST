from naoqi import ALProxy
from naoqi import ALBroker
NAO_IP = "192.168.75.41"
myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)

recorder = ALProxy("ALAudioRecorder")
recorder.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, (1,0,0,0))
recorder.stopMicrophonesRecording()

player = ALProxy ("ALAudioPlayer")

fileId = player.loadFile("/home/nao/test.wav")
player.play(fileId)

# on command line: ssh-keygen -t rsa
# on command line: ssh-copy-id nao@192.168.75.41

import subprocess
subprocess.call(["scp", "nao@192.168.75.41:test.wav","."])

subprocess.call(["/Users/stefanstarflinger/Downloads/sox-14.4.2/sox", "test.wav","test.flac"])

subprocess.call(["gsutil", "cp","gs://audio-for-semtec/"])
# Emotion

import httplib

h1 = httplib.HTTPConnection('www.google.at')

import requests

token = 'ya29.c.Elo_BfQDEDnv30UfLRI4OMeohfGmzQw15W97we_6FCVF_qLE1AO4WOwKkFW6Vt2_-D-COqSlnoIL6PNYWAdfzGX1uWPpdWNj-FzESwvAdlvuaaXEdF-RhO3VNEI'
headers = {"Content-Type": "application/json", "Authorization": "Bearer "+token}
uri = "https://speech.googleapis.com/v1/speech:recognize"
data = json.load(open('sync-request.json'))

r = requests.post(uri, data=json.dumps(data), headers=headers)