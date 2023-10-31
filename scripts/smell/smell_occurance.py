from dataclasses import dataclass


@dataclass
class SmellOccurrance:
    occurance: int = 0
    correct_detection: int = 0
    incorrect_detection: int = 0
