from pprint import pprint
from intentBox import IntentAssistant

i = IntentAssistant()
i.load_folder("test/weather")
sentences = ["what is the weather",
             "weather tomorrow",
             "say the weather in london",
             "how is the weather in dubai",
             "when will the world end"]
for s in sentences:
    print(s)
    pprint(i.fuzzy_best(s, min_conf=0.65))
    print()