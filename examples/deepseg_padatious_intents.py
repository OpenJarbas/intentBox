from intentBox.padatious_extract import PadatiousExtractor

from pprint import pprint

# deepseg only
intents = PadatiousExtractor(use_deepseg=True, use_markers=True, use_coref=True)

weather = ["weather"]
hello = ["hey", "hello", "hi", "greetings"]
name = ["my name is {name}"]
joke = ["tell me a joke", "i want a joke", "say a joke", "tell joke"]
lights_on = ["turn on the lights", "lights on", "turn lights on", "turn the lights on"]
lights_off = ["turn off the lights", "lights off", "turn lights off", "turn the lights off"]
door_on = ["open the door", "open door", "open the doors"]
door_off = ["close the door", "close door", "close the doors"]
music = ["play music", "play some songs", "play heavy metal", "play some jazz", "play rock"]
call = ["call {person}", "phone {person}"]
greet_person = ["say hello to {person}", "tell {person} hello", "tell {person} i said hello"]

intents.register_intent("weather", weather)
intents.register_intent("hello", hello)
intents.register_intent("name", name)
intents.register_intent("joke", joke)
intents.register_intent("lights_on", lights_on)
intents.register_intent("lights_off", lights_off)
intents.register_intent("door_open", door_on)
intents.register_intent("door_close", door_off)
intents.register_intent("play_music", music)
intents.register_intent("greet_person", greet_person)
intents.register_intent("call_person", call)


def deepseg_only():
    global intents
    print("#####  DEEPSEG ONLY")
    # deepseg only
    # intents = PadatiousExtractor(use_deepseg=True, use_markers=False)
    intents.segmenter.use_markers = False
    intents.segmenter.use_coref = False
    test()


def deepseg_markers():
    global intents
    print("#####  DEEPSEG AND MARKERS")
    # intents = PadatiousExtractor(use_deepseg=True)
    intents.segmenter.use_markers = True
    intents.segmenter.use_coref = False
    test()


def deepseg_markers_coref():
    global intents
    print("#####  DEEPSEG AND MARKERS AND COREFERENCE RESOLUTION")
    # intents = PadatiousExtractor(use_deepseg=True, use_coref=True)
    intents.segmenter.use_coref = True
    intents.segmenter.use_markers = True
    test()


def test():
    sentences = [
        "turn off the lights open the door",
        "Call mom and tell her hello",
        "tell me a joke and the weather",
        "turn on the lights close the door",
        "close the door turn off the lights",
        "tell me a joke and order some pizza and turn on the lights and close the door and play some songs",
        "close the pod bay doors play some music"  # fail
    ]

    print("# _______________________________")
    print("# SEGMENT AND CALCULATE BEST INTENTS")
    print("# _______________________________")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intents(sent))
        print("_______________________________")


deepseg_markers_coref()
deepseg_markers()
deepseg_only()
