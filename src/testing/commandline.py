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