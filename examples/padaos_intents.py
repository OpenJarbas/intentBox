from pprint import pprint
from intentBox.parsers.padaos_extract import PadaosExtractor
intents = PadaosExtractor()

weather = ["weather"]
hello = ["hey", "hello", "hi", "greetings"]
name = ["my name is {name}"]
joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
lights_on = ["turn on the lights", "lights on", "turn lights on",
             "turn the lights on"]
lights_off = ["turn off the lights", "lights off", "turn lights off",
              "turn the lights off"]
door_on = ["open the door", "open door", "open the doors"]
door_off = ["close the door", "close door", "close the doors"]
music = ["play music", "play some songs", "play heavy metal",
         "play some jazz", "play rock", "play some music"]
pizza = ["order pizza", "get pizza", "buy pizza"]
call = ["call {person}", "phone {person}"]
greet_person = ["say hello to {person}", "tell {person} hello",
                "tell {person} i said hello"]

intents.register_intent("weather", weather)
intents.register_intent("hello", hello)
intents.register_intent("name", name)
intents.register_intent("joke", joke)
intents.register_intent("lights_on", lights_on)
intents.register_intent("lights_off", lights_off)
intents.register_intent("door_open", door_on)
intents.register_intent("door_close", door_off)
intents.register_intent("play_music", music)
intents.register_intent("pizza", pizza)
intents.register_intent("greet_person", greet_person)
intents.register_intent("call_person", call)

sentences = [
    "tell me a joke and say hello",
    "turn off the lights, open the door",
    "nice work! get me a beer",
    "Call mom and tell her hello",
    "tell me a joke and the weather",
    "turn on the lights close the door",
    "close the door turn off the lights",
    "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
    "close the pod bay doors play some music"  # fail
]
print(intents.manifest())
print("CALCULATE SINGLE INTENT")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intent(sent))
    print("_______________________________")

print("SEGMENT AND CALCULATE BEST INTENTS")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intents(sent))
    print("_______________________________")

print("FILTER BY SCORE INTENTS")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.filter_intents(sent))
    print("_______________________________")

print("SEGMENT AND FILTER")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intents_list(sent))
    print("_______________________________")
