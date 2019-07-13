from intentBox.padatious_extract import PadatiousExtractor

from pprint import pprint

intents = PadatiousExtractor()

weather = ["weather"]
hello = ["hey", "hello", "hi", "greetings"]
name = ["my name is {name}"]
joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
lights_on = ["turn on the lights", "lights on", "turn lights on", "turn the lights on"]
lights_off = ["turn off the lights", "lights off", "turn lights off", "turn the lights off"]
door_on = ["open the door", "open door", "open the doors"]
door_off = ["close the door", "close door", "close the doors"]
music = ["play music", "play some songs", "play heavy metal", "play some jazz", "play rock"]

intents.register_intent("weather", weather)
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
