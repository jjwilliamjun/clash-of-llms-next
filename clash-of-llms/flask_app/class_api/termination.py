"""Custom terminating conditions"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Termination:
    def __init__(self, round, alignment=100):
        self._round = int(round)
        self._alignment = int(alignment)