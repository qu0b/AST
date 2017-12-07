import time
from naoqi import ALProxy
from naoqi import ALBroker
NAO_IP = "192.168.75.41"
myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)


# Creates a proxy on the speech-recognition module
asr = ALProxy("ALSpeechRecognition")

asr.setLanguage("English")

# Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
vocabulary = ["home", "record", "test"]
asr.pause(True)
asr.setVocabulary(vocabulary, False)

# Start the speech recognition engine with user Test_ASR
asr.subscribe("Test_ASR")
print 'Speech recognition engine started'
time.sleep(20)
asr.unsubscribe("Test_ASR")