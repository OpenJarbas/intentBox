from intentBox.coreference import CoreferenceSolver

text = "My sister has a dog. She loves him"
print(CoreferenceSolver.replace_coreferences(text))
# My sister has a dog. my sister loves a dog.
print(CoreferenceSolver.contexts)
# {'him': 'a dog', 'she': 'my sister'}

text = "Turn on the light and change it to blue"
print(CoreferenceSolver.replace_coreferences(text))
# Turn on the light and change the light to blue

print(CoreferenceSolver.contexts)  # keeps adding from previous text
# {'him': 'a dog', 'it': 'the light', 'she': 'my sister'}

print(CoreferenceSolver.extract_replacements(text, "Turn on the light and change the light to blue"))
# {'it': ['the light']}


text = "call mom"
print(CoreferenceSolver.replace_coreferences(text))
# call mom

text = "tell her to buy eggs"
print(CoreferenceSolver.replace_coreferences_with_context(text))  # use previous utterance for context
# tell mom to buy eggs

text = "tell her to buy coffee"
print(CoreferenceSolver.replace_coreferences_with_context(text))   # use previous utterance for context
# tell mom to buy coffee

text = "tell her to buy milk"
print(CoreferenceSolver.replace_coreferences(text))   # no context available
# tell her to buy milk
