from intentBox import IntentExtractor, Segmenter

from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class AdaptExtractor(IntentExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = IntentDeterminationEngine()

    def register_entity(self, name, samples):
        for kw in samples:
            self.engine.register_entity(kw, name)

    def register_intent(self, name, samples, optional_samples=None):
        """

        :param name: intent_name
        :param samples: list of required registered entities (names)
        :param optional_samples: list of optional registered samples (names)
        :return:
        """
        optional_samples = optional_samples or []
        # structure intent
        intent = IntentBuilder(name)
        for kw in samples:
            intent.require(kw)
        for kw in optional_samples:
            intent.optionally(kw)
        self.engine.register_intent_parser(intent.build())
        return intent

    def calc_intent(self, utterance):
        for intent in self.engine.determine_intent(utterance):
            if intent and intent.get('confidence') > 0:
                intent.pop("target")
                matches = [k for k in intent.keys() if k not in ["intent_type", "confidence"]]
                intent["matches"] = {}
                for k in matches:
                    intent["matches"][k] = intent[k]
                    intent.pop(k)
                intent["conf"] = intent["confidence"]
                intent.pop("confidence")
                return intent
        return {"conf": 0, "intent_type": "unknown", "matches": {}}

    def calc_intents(self, utterance, min_conf=0.5):
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            intent = self.calc_intent(ut)
            if intent["conf"] < min_conf:
                bucket[ut] = None
            else:
                bucket[ut] = intent
        return bucket

    def calc_intents_list(self, utterance, min_conf=0.5):
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = []
            for intent in self.engine.determine_intent(ut):
                if intent and intent.get('confidence') > 0:
                    intent.pop("target")
                    matches = [k for k in intent.keys() if k not in ["intent_type", "confidence"]]
                    intent["matches"] = {}
                    for k in matches:
                        intent["matches"][k] = intent[k]
                        intent.pop(k)
                    intent["conf"] = intent["confidence"]
                    intent.pop("confidence")
                    bucket[ut] += [intent]
            if not bucket[ut]:
                bucket[ut] = None
        return bucket


if __name__ == "__main__":
    from pprint import pprint

    intents = AdaptExtractor()

    weather = ["weather"]
    hello = ["hey", "hello", "hi", "greetings"]
    name = ["name is"]
    joke = ["joke"]
    play = ["play"]
    say = ["say", "tell"]
    music = ["music", "jazz", "metal", "rock"]
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
        "tell me a joke order some pizza",  # fail
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

    print("SEGMENT AND CALCULATE ALL INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intents_list(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intents_remainder(sent))
        print("_______________________________")
