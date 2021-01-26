from intentBox import Segmenter

s = Segmenter()

sentences = [
    "tell me a joke and say hello",
    "turn off the lights, open the door",
    "nice work! get me a beer",
    'I am Batman i live in gotham',
    "The romans discovered london they named it londinum",
    "Call mom tell her hello",
    "tell me a joke and the weather",
    "turn on the lights close the door",
    "close the door turn off the lights",
    "tell me a joke order some pizza",  # fail
    "close the pod bay doors play some music"  # fail
]

for sent in sentences:
    print(sent)
    print(s.segment(sent))
    print("___")
