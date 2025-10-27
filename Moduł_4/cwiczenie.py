import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("Debug message")

'''
Z dokumentacji https://docs.python.org/3/howto/logging.html#logging-to-a-file :

The call to basicConfig() should come before any calls to a logger’s methods such as debug(), info(), etc.
Otherwise, that logging event may not be handled in the desired manner.
'''
logging.basicConfig(level=logging.WARNING)  # NIE ZADZIAŁA!

logging.debug("Debug message")  # WYDRUKUJE SIĘ W KONSOLI!
logging.warning("Watch out!")