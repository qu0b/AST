import sys
sys.path.append("/Users/stefanstarflinger/Downloads/naoqi")
import time
from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "192.168.75.41", 9559)
tts.say("Yes im am sure")