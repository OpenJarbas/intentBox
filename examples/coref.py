from intentBox.coreference.pronoun_postags import PronounCoreferenceSolver


goods = [
    "My neighbors have a cat. It has a bushy tail.",
    "Here is the book now take it.",
    "The sign was too far away for the boy to read it.",
    "Dog is man's best friend. It is always loyal.",
    "The girl said she would take the trash out.",
    "I voted for Nader because he is clear about his values. His ideas represent a majority of the nation. He is better than Rajeev.",
    "Jack von Doom is one of the top candidates in the elections. His ideas are unique compared to Neha's.",
    "Members voted for John because they see him as a good leader.",
    "Leaders around the world say they stand for peace.",
    "My neighbours just adopted a puppy. They care for it like a baby.",
    "I have many friends. They are an important part of my life.",
    "London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium."
]

for s in goods:
    print(PronounCoreferenceSolver.replace_coreferences(s))
