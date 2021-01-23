import signal
import sys

def sigint_handler(signal, frame):
    print("\n")
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)