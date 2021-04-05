from intentBox.coreference.base import CoreferenceSolver
import spacy
import neuralcoref


class NeuralCoreferenceSolver(CoreferenceSolver):
    """https://github.com/huggingface/neuralcoref"""
    nlp = None

    def __init__(self, nlp=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO localize
        self.bind(nlp)

    @staticmethod
    def load_model(model="en"):
        # Load your usual SpaCy model (one of SpaCy English models)
        nlp = spacy.load(model)
        # Add neural coref to SpaCy's pipe
        neuralcoref.add_to_pipe(nlp)
        return nlp

    @classmethod
    def bind(cls, nlp=None):
        CoreferenceSolver.nlp = nlp or NeuralCoreferenceSolver.load_model()

    @classmethod
    def replace_coreferences(cls, text):
        cls.prev_sentence = text
        if text in cls.cache:
            solved = cls.cache[text]
        else:
            try:
                doc = cls.nlp(text)
                solved = doc._.coref_resolved
                cls.cache[text] = solved
            except Exception as e:
                cls.prev_solved = text
                return text
        extracted = cls.extract_replacements(text, solved)
        for pronoun in extracted:
            if len(extracted[pronoun]) > 0:
                cls.contexts[pronoun] = extracted[pronoun][-1]
        cls.prev_solved = solved
        return solved

    @classmethod
    def replace_coreferences_with_context(cls, text):
        if text in cls.cache:
            solved = cls.cache[text]
        else:
            new_text = cls.prev_solved + "; " + text
            try:
                doc = cls.nlp(new_text)
                solved = doc._.coref_resolved
                solved = solved.replace(cls.prev_solved + "; ", "").strip()
                cls.cache[new_text] = solved
                cls.cache[text] = solved
            except Exception as e:
                cls.prev_solved = text
                return text
        extracted = cls.extract_replacements(text, solved)
        for pronoun in extracted:
            if len(extracted[pronoun]) > 0:
                cls.contexts[pronoun] = extracted[pronoun][-1]
        cls.prev_sentence = text
        cls.prev_solved = solved
        return solved

