# Anwendungen aus Semantischen Technologien

## Intorduction

Interactions between humans and computers have become common place. Although for robots to live alongside humans they need to possess some form of emotional intelligence. In this project we looked at how we can utilize the information harvested from natural language processing (NLP), to determine someone's sentiment. We especially looked at how emotionally intelligent a machine can become. The goal of this project is to maximise the emotional quotient of a robot. Similar to the IQ the emotional quotient is a scale of how emotionally intelligent someone is. The first step was to have a knowledge base of emotions as done by. 

The next step was to have scenarios created using a modeling procedure. These scenarios are depicted by a model. The user can create a scenario, which adjusts his environment to be in a specic state, depending on the user's mood. To be able to define scenarios it was necessary to create a Meta Model of the robots possible actions. The actions are then mapped to emotional values/moods from a knowledge base such as an ontology. **This has been achieved using SEMFIS, which helped us create an environment where users can define in what emotional state they have to be for an action from the robot to be made.** For future work, only a subset of actions needs to be classied by the users and the rest will be inferred. Additionally, fuzzy sets were also considered as an alternative and/or an addition to an ontology. It was even considered to integrate fuzzy sets into ontologies. 

Finally, a validation environment was created with a subset of the specic case. To validate the scenario, a NAO robot was used. The microphone and the Software Development Kit (SDK) was used to capture audio clips and to communicate these clips to the Google servers via a REST API. The rst response from the API (speech to text) would be used to send another request. The second request would return the overall sentiment of the previously sent text. The value was used by the NAO to adjust the current scenario where a scenario is the current state of all the IOT devices in the local environment. 

At first, we discuss a future case, how interactions between humans and machines will be in the next 15-20 years. Then a generic approach of how we would achieve the described future will be discussed. The technology necessary for the advancement will be evaluated. A specic case will be looked at of what is already possible. And, nally, we validated if the case actually works.

## Conceptulization

Below we will describe six scenarios. These scenarios will clearly show what we whish to implement in our project. Each scenario has a use case description detailing what exactly it tries to achieve. The second part of each scenario are the deliverables. These are the technologies/concepts that will be used/produced. The last part of each scenario are the key performance indicators. These are the values/variables that will be looked at to measure how successful our implementation is in fulfilling the described usecase.

### Scenario 1: Voice Interaction

#### 1.1 Use Case Description

Interaction between the NAO and the user to record audio files. Convert the Audio files to text and use them in scenario 3

#### 1.2 Deliverables

#### 1.3 Key Performance Indicators

### Scenario 2: Sentiment Analysis

#### 2.1 Use Case Description

Develop a server that can perform NLP on text.

#### 2.2 Deliverables

* NLP processing
  * Tokenization
  * Sentiment Analysis

#### 2.3 Key Performance Indicators

* Compare speech from the audio file to the converted text.
* Emotional Quotient

### Scenario 3: Smart Home controller

#### 3.1 Use Case Description

#### 3.2 Deliverables

#### 3.3 Key Performance Indicators

### Scenario 4:

#### 4.1 Use Case Description

#### 4.2 Deliverables

#### 4.3 Key Performance Indicators

### Scenario 5: Model Instances

#### 5.1 Use Case Description 

For the model to be able to connect to the outide and influence the smart home it needs to be connected to the IoT devices in some way.
![a picture of a model instance][model-instance]

#### 5.2 Deliverables

* Create model instances
* Query model
* Webservice Integration
#### 5.3 Key Performance Indicators
* Interoperability
* Performance
* Useability
### Scenario 6 metamodel
#### 6.1 Use Case Description
To make it possible for someone to control their own home, a modelling language needs to be created. Through the modelling language the user will be able to control their smart home. We are talking about a smart home in which the lights can be adjusted depending on a certain criteria/emotion that the user can predetermine. This definition needs to be recorded in some way, such as in a model. Using a model to describe a smart home will enable alot of automation and will reduce setup time. Integrating different modelling procedures will let the user start up quickly and control their smart home however they desire. 

The users need a language i.e. a metamodel through which they can describe the relationships and entities that are in his smart home. In other words, the user needs a metamodel that lets the user create a model, which can control not only his smart home but also lets the user describe emotions inside of the model. The metamodel should define an abstract conceptuilzation of the objects in a smart home and of human emotions. By giving the user the possibility of creating models that can describe facts as well as emotions we are able to give a smart home emotional intelligence. This is limited to the extent that the user can only predefine specific scenarios and a model instance will not learn (from) the behaviour of the user.

#### 6.2 Deliverables

* Create a Metamodel
* Modelling Prcedures
* Graphrep

#### 6.3 Key Performance Indicators

* Easy to distinguish between objects (lookup in dem script)

## Development

## Deployment

## Conclusion

We have created a validating environment that checks whether
or not The NAO robot is emotionally intelligent in his actions. If the validation environment runs multiple test cases and each of them succeeds then the validation method would also be a success. The test cases should not require humans to monitor the system but a predened test set with an estimated sentiment polarity should be used to see if the system is operational. Further, the system should validate the resulting state of the IOT devices with the Graphrep representation in the Model. We are not too far away from having a fully functional robot that can interpret our emotions. The difficulty comes in having to ensure that the interpretation is correct. In the future, it would be interesting to see what other devices in our environment could be controlled by our emotions. IOT in the future allows for everything to change without the user directly interacting with the system. The NAO bot could detect if the person was cold and adjust the heating.

[//]: # (Image References)
[model-instance]: ./1209919_OmirobCase/home.png "Model Instance"