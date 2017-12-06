# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "192.168.75.41"
vocabulary = ["Hello", "Nao"]


# Global variable to store the HumanGreeter module instance
SoundDetection = None
memory = None
asr = None


class SoundDetectionModule(ALModule):
    """ A simple module able to react
    to sound detection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker
        global asr
        # Create a proxy to ALTextToSpeech for later use
        asr = ALProxy("ALSpeechRecognition")
        self.tts = ALProxy("ALTextToSpeech")
        #asr.setLanguage("English")
        #asr.setVocabulary(["Hello, Nao"], False)



        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")

    def onWordRecognized(self, key, value, message):
        """ This will be called each time a word is
        recognized.
        """
        memory.unsubscribeToEvent("WordRecognized", "SoundDetection")
        if(len(value) > 1 and value[1] >= 0.4):
          self.tts.say("How are you today")
        else:
          self.tts.say("I didnt Catch that")
        time.sleep(2)
        memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")


    def unsubscribe(self):
      self.asr.unsubscribe("Test_ASR")
        


def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global SoundDetection
    SoundDetection = SoundDetectionModule("SoundDetection")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()