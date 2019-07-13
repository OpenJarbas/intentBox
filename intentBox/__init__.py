import abc
from os.path import join, dirname


class Segmenter:
    # NOTE str.split operation, not token by token comparison
    # this means you need spaces on both sides of the marker

    # Add lang markers here
    markers = {
        "generic": ["\n", ".", "?", "!", ";", ","],
        "pt": [" e "],
        "en": [" and "]
    }

    def __init__(self, lang="en-us", use_markers=True, use_coref=False, use_deepseg=False,
                 model=join(dirname(__file__), "deepsegment_eng_fra_ita_v1/config.json")):
        self.lang = lang
        self.use_deepseg = use_deepseg
        self.use_markers = use_markers
        self.use_coref = use_coref
        self.segmenter = None
        self.solver = None
        if self.use_deepseg:
            if model == join(dirname(__file__), "deepsegment_eng_fra_ita_v1/config.json") and\
                    (not lang.startswith("en") or not lang.startswith("fr") or not lang.startswith("it")):
                    print("ERROR: unsupported deepsegment language")
            else:
                from deepsegment import DeepSegment
                self.segmenter = DeepSegment(model)
        if self.use_coref:
            if not lang.startswith("en"):
                print("ERROR: unsupported coreference resolution language")
            else:
                from intentBox.coreference import CoreferenceSolver
                # TODO check for neuralcoref, don't use the webdemos
                self.solver = CoreferenceSolver()

    @staticmethod
    def _extract(text, markers):
        if isinstance(text, str):
            sents = [text]
        else:
            sents = text
        flatten = lambda l: [item for sublist in l for item in sublist]
        for m in markers:
            for idx, sent in enumerate(sents):
                if isinstance(sent, str):
                    sents[idx] = sents[idx].split(m)
            # flatten list
            sents = flatten(sents)
        return sents

    @staticmethod
    def extract_candidates_en(text):
        sents = Segmenter.extract_candidates_generic(text)
        return Segmenter._extract(sents, Segmenter.markers["en"])

    @staticmethod
    def extract_candidates_pt(text):
        sents = Segmenter.extract_candidates_generic(text)
        return Segmenter._extract(sents, Segmenter.markers["pt"])

    @staticmethod
    def extract_candidates_generic(text):
        return Segmenter._extract(text, Segmenter.markers["generic"])

    @staticmethod
    def extract_candidates(text, lang="en"):
        if lang.startswith("en"):
            return Segmenter.extract_candidates_en(text)
        elif lang.startswith("pt"):
            return Segmenter.extract_candidates_pt(text)
        return Segmenter.extract_candidates_generic(text)

    def deepsegmentation(self, text):
        return self.segmenter.segment(text)

    def segment(self, text):
        if self.use_coref and self.solver:
            text = self.solver.replace_coreferences(text)
        if self.use_deepseg and self.segmenter:
            text = self.deepsegmentation(text)
        if self.use_markers:
            text = self.extract_candidates(text, self.lang)
        return [s for s in text if s]


class IntentExtractor:
    def __init__(self, lang="en-us", use_markers=True, use_coref=False, use_deepseg=False,
                 model=join(dirname(__file__), "deepsegment_eng_fra_ita_v1/config.json")):
        self.segmenter = Segmenter(lang, use_markers, use_coref, use_deepseg, model)

    @abc.abstractmethod
    def register_entity(self, name, samples):
        pass

    @abc.abstractmethod
    def register_intent(self, name, samples):
        pass

    @abc.abstractmethod
    def calc_intent(self, utterance):
        """ return intent result for utterance

       UTTERANCE: tell me a joke and say hello

        {'name': 'joke', 'sent': 'tell me a joke and say hello', 'matches': {}, 'conf': 0.5634853146417653}

        """
        pass

    @abc.abstractmethod
    def calc_intents(self, utterance, min_conf=0.5):
        """ segment utterance and return best intent for individual segments

        if confidence is bellow min_conf intent is None

       UTTERANCE: tell me a joke and say hello

        {'say hello': {'conf': 0.5750943775957492, 'matches': {}, 'name': 'hello'},
         'tell me a joke': {'conf': 1.0, 'matches': {}, 'name': 'joke'}}

        """
        pass

    @abc.abstractmethod
    def calc_intents_list(self, utterance):
        """ segment utterance and return all intents for individual segments

       UTTERANCE: tell me a joke and say hello

        {'say hello': [{'conf': 0.1405158302488502, 'matches': {}, 'name': 'weather'},
                       {'conf': 0.5750943775957492, 'matches': {}, 'name': 'hello'},
                       {'conf': 0.0, 'matches': {}, 'name': 'name'},
                       {'conf': 0.36216947883621736, 'matches': {}, 'name': 'joke'}],
         'tell me a joke': [{'conf': 0.0, 'matches': {}, 'name': 'weather'},
                            {'conf': 0.0, 'matches': {}, 'name': 'hello'},
                            {'conf': 0.0, 'matches': {}, 'name': 'name'},
                            {'conf': 1.0, 'matches': {}, 'name': 'joke'}]}

        """
        pass

    def intent_remainder(self, utterance):
        bucket = {"utterance": utterance,
                  "utterance_remainder": "",
                  "main_intent": None,
                  "remainder_intent": None}
        intent = self.calc_intent(utterance)
        bucket["main_intent"] = intent
        if len(intent.get("matches", {})):
            for m in intent["matches"]:
                utterance = utterance.replace(intent["matches"][m], "")
            bucket["utterance_remainder"] = utterance
            bucket["remainder_intent"] = self.calc_intent(utterance)
        return bucket

    def intents_remainder(self, utterance, min_conf=0.5):
        utterances = self.segmenter.segment(utterance)
        bucket = {}
        for utterance in utterances:
            bucket[utterance] = {"utterance": utterance,
                                 "utterance_remainder": "",
                                 "main_intent": None,
                                 "remainder_intent": None}
            intent = self.calc_intent(utterance)
            bucket[utterance]["main_intent"] = intent
            if len(intent.get("matches", {})):
                utterance_remainder = utterance
                for m in intent["matches"]:
                    utterance_remainder = utterance_remainder.replace(intent["matches"][m], "")
                bucket[utterance]["utterance_remainder"] = utterance_remainder
                bucket[utterance]["remainder_intent"] = self.calc_intent(utterance_remainder)
        return bucket


if __name__ == "__main__":
    s = Segmenter(use_deepseg=True)

    sentences = [
        "tell me a joke and say hello",
        "turn off the lights, open the door",
        "nice work! get me a beer",
        'I am Batman i live in gotham',
        "The romans discovered london they named it londinum",
        "Call mom tell her hello",
        "tell me a joke and the weather",
        "turn on the lights close the door",
        "close the door turn off the lights",
        "tell me a joke order some pizza",  # fail
        "close the pod bay doors play some music"  # fail
    ]

    for sent in sentences:
        print(sent)
        print(s.segment(sent))
        print("___")
