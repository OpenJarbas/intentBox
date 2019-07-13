
# intentBox

Multiple intent extraction from a single utterance, framed as a segmentation problem

- [About](#about)
  * [Single Intent](#single-intent)
    + [Adapt](#adapt)
    + [Padatious](#padatious)
  * [Main and Secondary intents](#main-and-secondary-intents)
    + [Adapt](#adapt-1)
  * [Segmentation + Intent](#segmentation---intent)
    + [Adapt](#adapt-2)
    + [Padatious](#padatious-1)
  * [Segmentation + Main and Secondary Intents](#segmentation---main-and-secondary-intents)
    + [Adapt](#adapt-3)
  * [Improving accuracy](#improving-accuracy)  
    + [DeepSegment](#deepsegment)
    + [Coreference resolution](#coreference-resolution)
- [Usage](#usage)
  * [Adapt](#adapt-4)
  * [Padatious](#padatious-2)


# About

## Single Intent

CONS: 
   - restricted to 1 utterance, 1 intent
   - mixes up conflicting orders into a single one

### Adapt

MAX: 1 intent

    UTTERANCE: turn off the lights and turn on the tv
    {'conf': 0.5,
     'intent_type': 'lights_on',
     'entities': {'lights': 'lights', 'on': 'on'}}
    _______________________________

    UTTERANCE: tell me a joke and the weather
    {'conf': 0.6666666666666666,
     'intent_type': 'weather',
     'entities': {'say': 'tell', 'weather': 'weather'}}
  
### Padatious

MAX: 1 intent

    UTTERANCE: tell me a joke order some pizza
    {'conf': 0.5230809565835034, 'entities': {}, 'name': 'joke'}    
    

## Main and Secondary intents

calculate an intent, remove entities from utterance, calculate intent in utterance remainer

PROS: 
- 1 utterance, 2 intents
- does not depend on segmentation
      
CONS: 
- loses context of keywords consumed in first intent
- it's not very smart joining keywords
- limited number of intents


### Adapt

adapt is keyword based so this works great, there always is an utterance remainder unless every word was consumed

MAX: 2 intents

    UTTERANCE: turn off the lights turn on the tv
    {'main_intent': {'conf': 0.5,
                     'intent_type': 'lights_on',
                     'entities': {'lights': 'lights', 'on': 'on'}},
     'remainder_intent': {'conf': 1.0,
                          'intent_type': 'tv_off',
                          'entities': {'tv': 'tv', 'off': 'off'}},
     'utterance': 'turn off the lights turn on the tv',
     'utterance_remainder': 'turn off the   the tv'}
    ______________________________
    UTTERANCE: turn on the lights close the door
    {'main_intent': {'conf': 0.5,
                     'intent_type': 'lights_on',
                     'entities': {'lights': 'lights', 'on': 'on'}},
     'remainder_intent': {'conf': 1.0,
                          'intent_type': 'door_close',
                          'entities': {'door': 'door', 'off': 'close'}},
     'utterance': 'turn on the lights close the door',
     'utterance_remainder': 'turn  the  close the door'}

     
     
padatious is examples based, there is no utterance remainder to use in this method


## Segmentation + Intent

works great in general

PROS: 

- uses segmentation to split utterances logically
- 1 utterance, unlimited intents
    
CONS: 

- context is lost in segmentation

### Adapt

MAX: number of utterance chunks after segmentation

    UTTERANCE: turn off the lights and open the door
    {' open the door': {'conf': 1.0,
                        'intent_type': 'door_open',
                        'entities': {'door': 'door', 'on': 'open'}},
     'turn off the lights': {'conf': 1.0,
                             'intent_type': 'lights_off',
                             'entities': {'lights': 'lights', 'off': 'off'}}}
                                                             
### Padatious

MAX: number of utterance chunks after segmentation

    UTTERANCE: tell me a joke and order some pizza and turn on the lights and close the door and play some songs
    {'close the door': {'conf': 1.0, 'entities': {}, 'name': 'door_close'},
     'order some pizza': None,
     'play some songs': {'conf': 1.0, 'entities': {}, 'name': 'play_music'},
     'tell me a joke': {'conf': 1.0, 'entities': {}, 'name': 'joke'},
     'turn on the lights': {'conf': 1.0, 'entities': {}, 'name': 'lights_on'}}
    _______________________________

## Segmentation + Main and Secondary Intents

same as above, works great in adapt but not usually in padatious

PROS: 
   - compensates for failures in segmentation

### Adapt

 MAX: 2* number of utterance chunks after segmentation

    UTTERANCE: close the pod bay doors play some music
    {'close the pod bay doors play some music': {'main_intent': {'conf': 0.5,
                                                                 'intent_type': 'door_close',
                                                                 'entities': {'door': 'doors',
                                                                             'off': 'close'}},
                                                 'remainder_intent': {'conf': 1.0,
                                                                      'intent_type': 'play_music',
                                                                      'entities': {'music': 'music',
                                                                                  'play': 'play'}},
                                                 'utterance': 'close the pod bay '
                                                              'doors play some '
                                                              'music',
                                                 'utterance_remainder': ' the pod '
                                                                        'bay  play '
                                                                        'some '
                                                                        'music'}} 
    
    


## Improving accuracy

### DeepSegment

Instead of rule based segmentantion we can handle more corner cases using [DeepSegment](https://github.com/bedapudi6788/deepsegment)

PROS: 
   - better segmentation, not rule based
   
CONS:
   - slows down pipeline
   - requires tensorflow
   
Cases where simple segmentation fails and this works:

    UTTERANCE: turn on the lights close the door
    {'close the door': {'conf': 1.0, 'entities': {}, 'name': 'door_close'},
     'turn on the lights': {'conf': 1.0, 'entities': {}, 'name': 'lights_on'}}
    _______________________________
    UTTERANCE: close the door turn off the lights
    {'close the door': {'conf': 1.0, 'entities': {}, 'name': 'door_close'},
     'turn off the lights': {'conf': 1.0, 'entities': {}, 'name': 'lights_off'}}
    
Failure cases

    UTTERANCE: turn off the lights open the door
    {'turn off the lights open the door': {'conf': 0.5311372507542608,
                                           'entities': {},
                                           'name': 'lights_off'}}]
    ___
    


### Coreference resolution

using [neuralcoref](https://github.com/huggingface/neuralcoref)


PROS: 
   - helps in keeping context
   
CONS:
   - slows down pipeline
   - requires spacy
   
segmentation only:

    UTTERANCE: Call mom and tell her hello
    {'Call mom': {'conf': 1.0,
                  'entities': {'person': 'mom'},
                  'name': 'call_person'},
     'tell her hello': {'conf': 1.0,
                        'entities': {'person': 'her'},
                        'name': 'greet_person'}}
    _______________________________

with coreference resolution

    UTTERANCE: Call mom and tell her hello
    {'Call mom': {'conf': 1.0,
                  'entities': {'person': 'mom'},
                  'name': 'call_person'},
     'tell mom hello': {'conf': 1.0,
                        'entities': {'person': 'mom'},
                        'name': 'greet_person'}}
    _______________________________



# Usage

## Adapt

```python
from intentBox.adapt_extract import AdaptExtractor

from pprint import pprint

intents = AdaptExtractor()
# intents = AdaptExtractor(use_deepseg=True)

weather = ["weather"]
hello = ["hey", "hello", "hi", "greetings"]
name = ["name is"]
joke = ["joke"]
play = ["play"]
say = ["say", "tell"]
music = ["music", "jazz", "metal", "rock", "songs"]
door = ["door", "doors"]
light = ["light", "lights"]
on = ["activate", "on", "engage", "open"]
off = ["deactivate", "off", "disengage", "close"]


intents.register_entity("weather", weather) # name, samples
intents.register_entity("hello", hello)
intents.register_entity("name", name)
intents.register_entity("joke", joke)
intents.register_entity("door", door)
intents.register_entity("lights", light)
intents.register_entity("on", on)
intents.register_entity("off", off)
intents.register_entity("play", play)
intents.register_entity("music", music)
intents.register_entity("say", say)


intents.register_intent("weather", ["weather"], ["say"]) # name, required_kwords, optional_kwords
intents.register_intent("hello", ["hello"])
intents.register_intent("name", ["name"])
intents.register_intent("joke", ["joke"], ["say"])
intents.register_intent("lights_on", ["lights", "on"])
intents.register_intent("lights_off", ["lights", "off"])
intents.register_intent("door_open", ["door", "on"])
intents.register_intent("door_close", ["door", "off"])
intents.register_intent("play_music", ["play", "music"])

sentences = [
    "tell me a joke and say hello",
    "turn off the lights, open the door",
    "nice work! get me a beer",
    "Call mom tell her hello",
    "tell me a joke and the weather",
    "turn on the lights close the door",
    "close the door turn off the lights",
    "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
    "close the pod bay doors play some music"  # fail
]

print("# _______________________________")
print("# CALCULATE SINGLE INTENT")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intent(sent))
    print("_______________________________")

print("# _______________________________")
print("# CALCULATE MAIN AND SECONDARY INTENTS")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.intent_remainder(sent))
    print("_______________________________")

print("# _______________________________")
print("# SEGMENT AND CALCULATE BEST INTENTS")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intents(sent))
    print("_______________________________")

print("# _______________________________")
print("# SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.intents_remainder(sent))
    print("_______________________________")

```
## Padatious


```python
from intentBox.padatious_extract import PadatiousExtractor

from pprint import pprint

intents = PadatiousExtractor()
# intents = PadatiousExtractor(use_deepseg=True) 


weather = ["weather"]
hello = ["hey", "hello", "hi", "greetings"]
name = ["my name is {name}"]
joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
lights_on = ["turn on the lights", "lights on", "turn lights on", "turn the lights on"]
lights_off = ["turn off the lights", "lights off", "turn lights off", "turn the lights off"]
door_on = ["open the door", "open door", "open the doors"]
door_off = ["close the door", "close door", "close the doors"]
music = ["play music", "play some songs", "play heavy metal", "play some jazz", "play rock"]

intents.register_intent("weather", weather)  # name, samples
intents.register_intent("hello", hello)
intents.register_intent("name", name)
intents.register_intent("joke", joke)
intents.register_intent("lights_on", lights_on)
intents.register_intent("lights_off", lights_off)
intents.register_intent("door_open", door_on)
intents.register_intent("door_close", door_off)
intents.register_intent("play_music", music)

sentences = [
    "tell me a joke and say hello",
    "turn off the lights, open the door",
    "nice work! get me a beer",
    "Call mom tell her hello",
    "tell me a joke and the weather",
    "turn on the lights close the door",
    "close the door turn off the lights",
    "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
    "close the pod bay doors play some music"  # fail
]

print("# _______________________________")
print("# CALCULATE SINGLE INTENT")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intent(sent))
    print("_______________________________")

print("# _______________________________")
print("# SEGMENT AND CALCULATE BEST INTENTS")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intents(sent))
    print("_______________________________")

```

## Coreference

```python

from intentBox.coreference import CoreferenceSolver

text = "My sister has a dog. She loves him"
print(CoreferenceSolver.replace_coreferences(text))
# My sister has a dog. my sister loves a dog.
print(CoreferenceSolver.contexts)
# {'him': 'a dog', 'she': 'my sister'}

text = "Turn on the light and change it to blue"
print(CoreferenceSolver.replace_coreferences(text))
# Turn on the light and change the light to blue

print(CoreferenceSolver.contexts)  # keeps adding from previous text
# {'him': 'a dog', 'it': 'the light', 'she': 'my sister'}

print(CoreferenceSolver.extract_replacements(text, "Turn on the light and change the light to blue"))
# {'it': ['the light']}


text = "call mom"
print(CoreferenceSolver.replace_coreferences(text))
# call mom

text = "tell her to buy eggs"
print(CoreferenceSolver.replace_coreferences_with_context(text))  # use previous utterance for context
# tell mom to buy eggs

text = "tell her to buy coffee"
print(CoreferenceSolver.replace_coreferences_with_context(text))   # use previous utterance for context
# tell mom to buy coffee

text = "tell her to buy milk"
print(CoreferenceSolver.replace_coreferences(text))   # no context available
# tell her to buy milk

```