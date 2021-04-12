from pprint import pprint
import os
from intentBox import IntentAssistant

i = IntentAssistant()

p = "/home/user/my_code/MycroftDefaultSkills"
for skill in os.listdir(p):
    if os.path.isdir(os.path.join(p, skill)):
        i.load_mycroft_skill(os.path.join(p, skill), adapt=False)

#### WARNING THIS IS SLOW
print("\nADAPT:")
for intent_name, intent in i.adapt_intents.items():
    print(intent_name)
    pprint(intent)
    print("########")


