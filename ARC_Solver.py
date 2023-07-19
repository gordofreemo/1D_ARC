import json, typing, os
from enum import Enum

class Color(Enum):
    BLACK = 0
    DARK_BLUE = 1
    RED = 2
    GREEN =  3
    YELLOW = 4
    GRAY = 5
    PINK = 6
    ORANGE = 7
    LIGHT_BLUE = 8
    DARK_RED = 9

ARC_Grid = list[Color]
ARC_Object = dict[int, int, ARC_Grid]
ARC_Pair = tuple[ARC_Grid, ARC_Grid]

class ARC_Test:
    demonstrations : list [ARC_Pair]
    tests : list[ARC_Pair]
    def __init__(self, demonstrations : list [ARC_Pair], tests : list[ARC_Pair]) -> None:
        self.demonstrations = demonstrations
        self.tests = tests
    def __init__(self, file_name : str) -> None:
        self.parse_ARC_tests(file_name)
    def parse_ARC_tests(self, file_name : str) -> None:
        fp : __file__ = None
        try:
            fp = open(file_name, 'r')
        except:
            return None
        data : dict = json.load(fp) 
        fp.close()
        # Convert training data to list of tuples w/ input/output color pairs
        self.demonstrations = [(list(map(Color, x['input'][0])), list(map(Color,x['output'][0]))) for x in data['train']]
        self.tests  = [(list(map(Color, x['input'][0])), list(map(Color,x['output'][0]))) for x in data['test']]