from pprint import pprint
from intentBox import IntentBox, IntentDeterminationStrategy

intents = IntentBox(strategy=IntentDeterminationStrategy.SEGMENT_REMAINDER)

# sample based intents

weather = ["weather"]
hello = ["hey", "hello", "hi", "greetings"]
joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
lights_on = ["turn on the lights", "lights on", "turn lights on", "turn the lights on"]
lights_off = ["turn off the lights", "lights off", "turn lights off", "turn the lights off"]
music = ["play music", "play some songs", "play heavy metal", "play some jazz", "play rock", "play some music"]
call = ["call {person}", "phone {person}"]

intents.register_intent("weather", weather)
intents.register_intent("hello", hello)
intents.register_intent("joke", joke)
intents.register_intent("lights_on", lights_on)
intents.register_intent("lights_off", lights_off)
intents.register_intent("play_music", music)
intents.register_intent("call_person", call)

# keyword based intents
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

intents.register_entity("weather", weather)
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

intents.register_adapt_intent("weather", ["weather"], ["say"])
intents.register_adapt_intent("hello", ["hello"])
intents.register_adapt_intent("name", ["name"])
intents.register_adapt_intent("joke", ["joke"], ["say"])
intents.register_adapt_intent("lights_on", ["lights", "on"])
intents.register_adapt_intent("lights_off", ["lights", "off"])
intents.register_adapt_intent("door_open", ["door", "on"])
intents.register_adapt_intent("door_close", ["door", "off"])
intents.register_adapt_intent("play_music", ["play", "music"])

sentences = [
    "turn off the lights, open the door",
    "Call mom and tell her hello",
    "tell me a joke and the weather",
    "turn on the lights close the door",
    "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
    "close the pod bay doors play some music",
    "play the music satan and friends"
]
print("# _______________________________")
print("# CALC")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc(sent))
    print("_______________________________")
exit(0)
print("# _______________________________")
print("# CALCULATE SINGLE INTENT")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intent(sent))
    print("_______________________________")

print("# _______________________________")
print("# FILTER BY THRESHOLD CONFIDENCE")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.filter_intents(sent, 0.5))
    print("_______________________________")

print("# _______________________________")
print("# SEGMENT AND CALCULATE BEST INTENTS")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intents(sent))
    print("_______________________________")

print("# _______________________________")
print("# SEGMENT AND CALCULATE ALL INTENTS")
print("# _______________________________")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.calc_intents_list(sent))
    print("_______________________________")

print("SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
for sent in sentences:
    print("UTTERANCE:", sent)
    pprint(intents.intents_remainder(sent))
    print("_______________________________")
