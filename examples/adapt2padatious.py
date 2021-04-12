from pprint import pprint
import os
from intentBox import IntentAssistant

i = IntentAssistant()

p = "/home/user/my_code/MycroftDefaultSkills"
for skill in os.listdir(p):
    if "weather" in skill:
        continue
    if os.path.isdir(os.path.join(p, skill)):
        i.load_mycroft_skill(os.path.join(p, skill), padatious=False)

#### WARNING THIS IS SLOW
print("\nPADATIOUS:")
for intent_name, intent in i.padatious_intents.items():
    intent = intent[0]
    print(intent_name)
    intent["samples"] = intent["samples"][:50]
    pprint(intent)
    print("########")


