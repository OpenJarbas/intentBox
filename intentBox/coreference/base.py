
class CoreferenceSolver:
    cache = {}
    contexts = {}
    prev_sentence = ""
    prev_solved = ""

    def __init__(self, lang="en-us"):
        self.lang = lang

    @staticmethod
    def extract_replacements(original, solved):
        a = original.lower()
        b = solved.lower()
        chunk = a.split(" ")
        chunk2 = b.split(" ")
        replaced = {}
        index_map = {}
        # extract keys
        indexes = []
        for idx, w in enumerate(chunk):
            if w not in chunk2:
                indexes.append(idx)
                replaced[idx] = []
                index_map[idx] = w
        i2 = 0
        for i in indexes:
            o = chunk[i:]
            s = chunk2[i + i2:]
            if len(o) == 1:
                # print(o[0], "->", " ".join(s), i)
                replaced[i].append(" ".join(s))
                continue
            for idx, word in enumerate(o):
                if word not in s:
                    chunk3 = s[idx:]
                    for idx2, word2 in enumerate(chunk3):
                        if word2 in o and not replaced[i]:
                            chunk3 = s[:idx2]
                            i2 += len(chunk3) - 1
                            # print(word, "->", " ".join(chunk3), i)
                            replaced[i].append(" ".join(chunk3))
        bucket = {}
        for k in replaced:
            if index_map[k] not in bucket:
                bucket[index_map[k]] = []
            bucket[index_map[k]] += replaced[k]
        return bucket

    @classmethod
    def replace_coreferences(cls, text):
        cls.prev_sentence = text
        if text in cls.cache:
            return cls.cache[text]
        else:
            return text

    @classmethod
    def replace_coreferences_with_context(cls, text):
        if text in cls.cache:
            solved = cls.cache[text]
        else:
            solved = text
        extracted = cls.extract_replacements(text, solved)
        for pronoun in extracted:
            if len(extracted[pronoun]) > 0:
                cls.contexts[pronoun] = extracted[pronoun][-1]
        cls.prev_sentence = text
        cls.prev_solved = solved
        return solved

