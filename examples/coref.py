from intentBox.coreference.remote import NeuralCoreferenceDemoSolver
from pprint import pprint


text = "My sister has a dog. She loves him"
print(NeuralCoreferenceDemoSolver.replace_coreferences(text))
# My sister has a dog. my sister loves a dog.
pprint(NeuralCoreferenceDemoSolver.contexts)
# {'him': 'a dog', 'she': 'my sister'}

text = "Turn on the light and change it to blue"
print(NeuralCoreferenceDemoSolver.replace_coreferences(text))
# Turn on the light and change the light to blue
pprint(NeuralCoreferenceDemoSolver.contexts)
# {'him': 'a dog', 'it': 'the light', 'she': 'my sister'}
print(NeuralCoreferenceDemoSolver.extract_replacements(text,
                                             "Turn on the light and change the light to blue"))
# {'it': ['the light']}

text = "London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium."
print(NeuralCoreferenceDemoSolver.replace_coreferences(text))
# London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia. london was founded by the Romans, who named london Londinium.
print(NeuralCoreferenceDemoSolver.prev_sentence)
# London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium.
print(
    NeuralCoreferenceDemoSolver.extract_replacements(NeuralCoreferenceDemoSolver.prev_sentence,
                                           NeuralCoreferenceDemoSolver.replace_coreferences(
                                               text)))
# {'it': ['london', 'london'], 'who': ['the romans']}

text = "call mom"
print(NeuralCoreferenceDemoSolver.replace_coreferences(text))
# call mom

text = "tell her to buy eggs"
print(NeuralCoreferenceDemoSolver.replace_coreferences_with_context(text))
# tell mom to buy eggs

text = "tell her to buy coffee"
print(NeuralCoreferenceDemoSolver.replace_coreferences_with_context(text))
# tell mom to buy coffee

text = "tell her to buy milk"
print(NeuralCoreferenceDemoSolver.replace_coreferences(text))
# tell her to buy milk
