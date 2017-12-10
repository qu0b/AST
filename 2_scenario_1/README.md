# Implementation of Scenario 1

### Table of contents

* [Implementation of scenario 1](#scenario1)
* [Outlook: Technology stack of all scenarios](#technologystack)


## <a name="scenario1"></a> Scenario 1: Recording raw audio data with NAO

From our conceptualization:

> In this first scenario we want to make it possible for the NAO to start and stop recording audio. The NAO needs to be aware when someone is talking to it in order to start recording. It also has to recognize when someone is done talking to stop the recording. 

> The purpose of this use case is to gather the necessary raw data for use cases 2 and 3 so that they can provide semantically meaningful information, knowledge and actions. 

*For the full description of the first scenario please refer to [our conceptualization submission](../1_conceptualization#scenario1).*

##### Set up connectivity with the NAO

We chose to work with the red NAO, however the steps to replicate this on the blue NAO are very similar. To connect with the NAO, we have to turn it on and connect to the same WLAN as the NAO. Once this is done we can connect via the browser at `192.168.75.41`. If there are connectivity issues `arp -a` command can help out for troubleshooting.

##### SDK

For the implemation we first had to choose a NAO SDK. Only two complete SDKs are written in `C++` and `Python`. We chose `Python` mostly because it is more intuitive to read and also because we can easily run code remotely from our machines. This will be useful for the second use case, since we will be able to run commands remotely from our server on the NAO.

##### File transfer

Since we need to access the audio files which we record on the NAO, we had to figure out a way to access these files. There are lots of options however we ended up deciding for `scp` protocol. The reason for this is mostly, that in our architecture the central component is not the NAO, but another centrilized component (e.g. a smart home automation or in our case a laptop). Since we need to get the audio recordings from the NAO to our machines, and invoke that transfer from our machines `scp` is very well suited for this task. It can be remotely invoked and is secure, fast and works over a local network. See the [documentation](http://nixdoc.net/man-pages/FreeBSD/scp.1.html) for more info. 

##### Optimization of speech recognition and recording

In our original concecptualization we wrote:

> The NAO needs to be aware when someone is talking to it in order to start recording. It also has to recognize when someone is done talking to stop the recording. 

However after extensive testing and with regard to the fact that we need to build two more use cases upon the audio files that we generate in this use case, we have decided to slightly adapt the use case. Here are some of the problems we encountered:

* The NAO is a lot less responsive in a conversation than we originally thought. It's hard to pinpoint when the NAO is going to speak, and when it is going to listen. Sometime the NAO seems to be unresponsive for short periods of time. It seems while it is a cool technology, concerning conversations the NAO is not 100% reliable. While trying out different ways to mitigate this, we mostly noticed that the behaviour is quite unpredictable.

* During a conversation the NAO will make lots of noises. He will sometimes speak and very often make loud 'beep sounds'. These sounds are there to indicate when the NAO is listening and to help the flow of conversation, however they turn out extremely loud in the resulting recorded audio file. 

* Additionally, the NAO speaks itself. So his own voice will be recorded in every clip. Since our goal is ultimately to interpret and work with the audio files this also can be considered problematic.

To mitigate these problems we have decided to slighty adapt our original conceptualization. We will make the NAO listen to a set of defined keywords, and then act upon that by recording for a fixed period of time.

This allows us to focus on the main goal of intepreting and analyzing the audio files. The NAO is part of the scenario because one day it will be possible to have a personal assistant robot which can interpret the emotions of his owner, and act accordingly. The purpose of this prototype is to get as close as possible to that goal. However it seems that the hardware of the NAO is not ideally suited for this use case. If the NAO had more suitable microphones or a software which could distinguish between his own noises and other noises this could be handled better in the future.

##### Overview of the code

*The full code for this prototype of scenario 1 can be found [here](hello_detection.py).*

The following is the most important part of the code.

```python
def onWordRecognized(self, key, value, message):

	try:
        memory.unsubscribeToEvent("WordRecognized", "SoundDetection")
        if(len(value) > 1 and value[1] >= 0.5):    
            self.tts.say("Recording")
            import subprocess
            recorder = ALProxy("ALAudioRecorder")
            self.tts.say("Starting recorder")
            recorder.stopMicrophonesRecording()
            recorder.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, (1,0,0,0))
            time.sleep(10)
            self.tts.say("stopping recorder")
            recorder.stopMicrophonesRecording()
            self.tts.say("copying audio file")
            subprocess.call(["scp", "nao@192.168.75.41:test.wav","."])
            memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")
        else:
            self.tts.say("I didnt Catch that")
            time.sleep(1)
            memory.subscribeToEvent("WordRecognized", "SoundDetection", "onWordRecognized")
    except:
        print("overload")
```

...

## <a name="technologystack"></a> Outlook: Technology stack of all scenarios

#### architecture

