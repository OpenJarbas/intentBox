from intentBox.intent_assistant.collision_detector import CollisionDetector

c = CollisionDetector("/home/user/chatterbox/skills")

print(c.triggered_skills("what is your ip address"))
print(c.triggered_skills("say that again"))
print(c.triggered_skills("what did i say"))

"""
[{'skill': 'ip_address', 'conf': 1.0, 'entities': {}, 'intent_name': 'intent_name2Intent', 'intent_engine': 'padatious'}]
[{'skill': 'volume', 'conf': 1.0, 'entities': {}, 'intent_name': 'intent_name3Intent', 'intent_engine': 'padatious'}]
[{'intent_name': 'say_that_again', 'entities': {'again:say_that_again': 'say that again'}, 'skill': 'again', 'conf': 1.0, 'intent_engine': 'adapt'}]
[{'intent_name': 'what_did_i_say', 'entities': {'again:what_did_i_say': 'what did i say'}, 'skill': 'again', 'conf': 1.0, 'intent_engine': 'adapt'}]
"""