from intentBox import IntentExtractor, Segmenter
from padatious import IntentContainer


class PadatiousExtractor(IntentExtractor):
    def __init__(self, cache_dir="/tmp/padatious", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = IntentContainer(cache_dir)

    def register_entity(self, name, samples):
        self.container.add_entity(name, samples)

    def register_intent(self, name, samples):
        self.container.add_intent(name, samples)

    def calc_intent(self, utterance, min_conf=0.5):
        intent = self.container.calc_intent(utterance).__dict__
        if intent["conf"] < min_conf:
            return {"name": "unknown", "entities": {}, "conf": 0}
        intent.pop("sent")
        intent["entities"] = intent["matches"]
        intent.pop("matches")
        return intent

    def calc_intents(self, utterance, min_conf=0.5):
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            intent = self.calc_intent(ut)
            if intent["conf"] < min_conf:
                bucket[ut] = None
            else:
                bucket[ut] = intent
        return bucket

    def calc_intents_list(self, utterance):
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = self.container.calc_intents(ut)
        return bucket


if __name__ == "__main__":
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

    print("CALCULATE SINGLE INTENT")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intent(sent))
        print("_______________________________")

    print("CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intent_remainder(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE BEST INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intents(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intents_remainder(sent))
        print("_______________________________")
