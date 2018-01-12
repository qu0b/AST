# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
import json
import requests

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
import xml.etree.ElementTree as ET

def excell():
    root = ET.parse('parse.xml')

    configs = []
    moods = []

    for elem in root.findall("//connector/from[@instance='NAO red']/../to"):
        # How to make decisions based on attributes even in 2.6:
        moods.append(elem.attrib['instance'])

    for mood in moods:
        tempobj = {'mood': mood, 'range': '', 'color': '', 'song': ''}
        for g in root.findall("//instance[@name='"+mood+"']//attribute[@name='Emotional range']"):
            tempobj['range'] = g.text
        for elem in root.findall("//connector/from[@instance='"+mood+"']/../to[@class='Color']"):
            for e in root.findall("//instance[@name='"+elem.attrib['instance']+"']//attribute[@name='Color']"):
                tempobj['color'] = e.text
        for elem in root.findall("//connector/from[@instance='"+mood+"']/../to[@class='Music']"):
            tempobj['song'] = elem.attrib['instance']
        configs.append(tempobj)
    return configs

NAO_IP = "192.168.75.41"
vocabulary = ["home", "record"]

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

        
        asr.setLanguage("English")
        asr.pause(True)
        asr.setVocabulary(vocabulary, False)
        asr.pause(False)
        asr.subscribe("Test_ASR")

        

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")

    def onWordRecognized(self, key, value, message):
        """ This will be called each time a word is
        recognized.
        """
        #try:
        memory.unsubscribeToEvent("WordRecognized", "SoundDetection")
        if(len(value) > 1 and value[1] >= 0.4):
            uri_cl1 = "http://192.168.75.105/api/TXfYgBPL5er0OGkZ9ZAsx6yeqBrdKzOk759Q-PA6/lights/1/state"
            requests.put(uri_cl1, json = {"effect":"colorwheel"}, headers = {'Content-Type': 'application/json'})
            self.tts.say("Recording")
            import subprocess
            recorder = ALProxy("ALAudioRecorder")
            self.tts.say("Starting recorder")
            recorder.stopMicrophonesRecording()
            recorder.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, (1,0,0,0))
            time.sleep(5)
            recorder.stopMicrophonesRecording()
            self.tts.say("stopping recorder, analyzing your mood")
            subprocess.call(["scp", "nao@192.168.75.41:test.wav","."])
            print("creating flac")
            subprocess.call(["/Users/stefanstarflinger/Downloads/sox-14.4.2/sox", "test.wav","test.flac"])
            print("copying audio file to google cloud")
            subprocess.call(["gsutil", "cp","test.flac","gs://audio-for-semtec/"])
            token_raw = subprocess.Popen(["gcloud", "auth", "application-default", "print-access-token"], stdout=subprocess.PIPE)
            token = token_raw.stdout.read()[:-1]
            headers = {"Content-Type": "application/json", "Authorization": "Bearer "+token}
            uri = "https://speech.googleapis.com/v1/speech:recognize"
            data = json.load(open('sync-request.json'))

            print("audio to text")
            r = requests.post(uri, json=data, headers=headers)
            print(r.text)
            text = json.loads(r.content)["results"][0]["alternatives"][0]["transcript"]
            print(text)
            data_sent = {"document": {"type": "PLAIN_TEXT", "content":text}, "encodingType":"UTF8"}
            print("sentiment analysis")
            uri_sent = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyA671KhhlHRqQ_ZxmVou7GaLct_b-Txdes'
            print("sentiment analysis resluts")
            r_sent = requests.post(uri_sent, json=data_sent)
            print(r.text)
            led = ALProxy("ALLeds")
            player = ALProxy ("ALAudioPlayer")
            key = "TXfYgBPL5er0OGkZ9ZAsx6yeqBrdKzOk759Q-PA6"
            uri_cl1 = "http://192.168.75.105/api/TXfYgBPL5er0OGkZ9ZAsx6yeqBrdKzOk759Q-PA6/lights/1/state"
            colors = {"Blue":{"on": True, "bri": 150, "hue": 5448, "sat": 233, "effect": "none", "xy": [ 0.1639, 0.1904 ], "ct": 500}, "Orange":{"on": True, "bri": 80, "hue": 15448, "sat": 233, "effect": "none", "xy": [ 0.5639, 0.4404 ], "ct": 500}, "Red":{"on": True, "bri": 80, "hue": 25448, "sat": 233, "effect": "none", "xy": [ 0.7339, 0.3904 ], "ct": 500}, "Purple":{"on": True, "bri": 87, "hue": 5448, "sat": 233, "effect": "none", "xy": [ 0.4639, 0.1904 ], "ct": 500}, "Green":{"on": True, "bri": 57, "hue": 5448, "sat": 233, "effect": "none", "xy": [ 0.1639, 0.8904 ], "ct": 500}}
            print('change led color')
            sentimentScore = float(json.loads(r_sent.content)["documentSentiment"]["score"])
            sent = ''
            if(sentimentScore >= 0.5):
                sent = "Very positive"
            elif(sentimentScore >= 0):
                sent = "Positive"
            elif(sentimentScore >=-0.7):
                sent = "Negative"
            elif(sentimentScore >=-1):
                sent = "Very negative"
                
            configs = excell()

            for config in configs:
                if(sent == config["range"]):
                    fileId = player.loadFile("/home/nao/"+config["song"]+".wav")
                    
                    requests.put(uri_cl1, json = colors[config["color"]], headers = {'Content-Type': 'application/json'})
                    player.play(fileId)
                    self.tts.say("you seem to be "+config["mood"])
                    col = config["color"]
                    if(col=="Orange"):
                        col="red"
                    
                    led.fadeRGB("AllLeds", col.lower(), 3)
                else: pass
            
            #if(sentimentScore > 0):
            #    fileId = player.loadFile("/home/nao/scream.wav")
            #    player.play(fileId)
            #    requests.put(uri_cl1, json = blue, headers = {'Content-Type': 'application/json'})
            #    self.tts.say("you seem to be happy")
            #    led.fadeRGB("AllLeds", "blue", 3)
            #else:
            #    requests.put(uri_cl1, json = candle, headers = {'Content-Type': 'application/json'})
            #    self.tts.say("you seem to be sad")
            #    led.fadeRGB("AllLeds", "red", 3)
            #    self.tts.say("awwwwwwwwwwwwww")
                
            print(r_sent.text)

            memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")
        else:
            self.tts.say("I didnt Catch that")
            time.sleep(1)
            memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")
        #except Exception:
          #  print(Exception)
        
        


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