import requests
from intentBox.lang.en import COREFERENCE_INDICATORS_EN
from intentBox.coreference.base import CoreferenceSolver


def neuralcoref_demo(text):
    try:
        params = {"text": text}
        r = requests.get("https://coref.huggingface.co/coref",
                         params=params).json()
        text = r["corefResText"] or text
    except Exception as e:
        pass
    return text


def cogcomp_coref_resolution(text):
    try:
        data = _cogcomp_demo(text)
        links = data["links"]
        node_ids = {}
        replace_map = {}
        for n in data["nodes"]:
            node_ids[int(n["id"])] = n["name"]
        for l in links:
            # TODO localization
            if node_ids[l["target"]].lower() not in COREFERENCE_INDICATORS_EN:
                continue
            replace_map[node_ids[l["target"]]] = node_ids[l["source"]]
        for r in replace_map:
            text = text.replace(r, replace_map[r])
        return text
    except Exception as e:
        return text


def _cogcomp_demo(text):
    url = "https://cogcomp.org/demo_files/Coref.php"
    data = {"lang": "en", "text": text}
    r = requests.post(url, json=data)
    return r.json()


class NeuralCoreferenceDemoSolver(CoreferenceSolver):
    @classmethod
    def replace_coreferences(cls, text):
        cls.prev_sentence = text
        if text in cls.cache:
            solved = cls.cache[text]
        else:
            try:
                solved = neuralcoref_demo(text)
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
                solved = neuralcoref_demo(new_text)
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


class CogCompDemoSolver(CoreferenceSolver):
    @classmethod
    def replace_coreferences(cls, text):
        cls.prev_sentence = text
        if text in cls.cache:
            solved = cls.cache[text]
        else:
            try:
                solved = cogcomp_coref_resolution(text)
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
                solved = cogcomp_coref_resolution(new_text)
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

