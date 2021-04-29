from intentBox.parsers.template import IntentExtractor
from palavreado import IntentContainer, IntentCreator


class PalavreadoExtractor(IntentExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intent_builders = {}
        self.engine = IntentContainer()

    def register_intent(self, name, samples=None, optional_samples=None):
        """

        :param name: intent_name
        :param samples: list of required registered entities (names)
        :param optional_samples: list of optional registered samples (names)
        :return:
        """
        if not samples:
            samples = [name]
        optional_samples = optional_samples or []

        # structure intent
        intent = IntentCreator(name)
        for kw in samples:
            intent.require(kw, [])
        for kw in optional_samples:
            intent.optionally(kw, [])
        self.intent_builders[name] = intent
        return intent

    def calc_intent(self, utterance):
        # update intents with registered entity samples
        for intent_name, intent in self.intent_builders.items():
            for kw, samples in self.registered_entities.items():
                if kw in intent.required:
                    intent.required[kw] = samples
                if kw in intent.optional:
                    intent.optional[kw] = samples
            self.engine.add_intent(intent)
        intent = self.engine.calc_intent(utterance)
        if intent.get("conf") > 0:
            intent["intent_engine"] = "palavreado"
            intent["intent_type"] = intent.pop("name")
            return intent
        return {"conf": 0, "intent_type": "unknown", "entities": {},
                "utterance": utterance, "utterance_remainder": utterance,
                "intent_engine": "palavreado"}


if __name__ == "__main__":
    from pprint import pprint

    intents = PalavreadoExtractor()

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

    print("SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intents_remainder(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE ALL INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intents_list(sent))
        print("_______________________________")
