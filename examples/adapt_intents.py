from intentBox.parsers.adapt_extract import AdaptExtractor

from pprint import pprint

intents = AdaptExtractor()

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

intents.register_intent("weather", ["weather"], ["say"])
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
