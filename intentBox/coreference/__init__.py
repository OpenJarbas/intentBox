from intentBox.lang.en import COREFERENCE_INDICATORS_EN
from intentBox.utils import tokenize
from intentBox.coreference.base import CoreferenceSolver


def replace_coreferences(text, smart=True, nlp=None):
    if smart:
        words = tokenize(text)
        should_solve = False
        for indicator in COREFERENCE_INDICATORS_EN:
            if indicator in words:
                should_solve = True
                break
        if not should_solve:
            return text
    solver = CoreferenceSolver(nlp)
    solved = solver.replace_coreferences(text)
    if solved == text:
        return solver.replace_coreferences_with_context(text)
    return solved


