from pprint import pprint
from intentBox import IntentAssistant

i = IntentAssistant()
i.load_folder("test/intents")

print("\nADAPT:")
pprint(i.adapt_intents)

print("\nPADATIOUS:")
pprint(i.padatious_intents)

print("\nFUZZY MATCH:")
pprint(i.fuzzy_intents)

