import re
import queue

varNameRegex: str = "[A-z][A-z0-9]*"
intRegex: int = "((\d)(_(?=\d))*)+"
floatRegex: str = "(\d(_(?=\d))*)+\.?(\d(_(?=\d))*)*"
boolRegex: str = "(T|t|F|f)(alse|ALSE|rue|RUE)"
hexRegex: str = "(#)?(([0-9A-Fa-f])(_(?=[0-9A-Fa-f]))*)+"

primitiveDict: dict = {
    "int": intRegex,
    "float": floatRegex,
    "bool": boolRegex,
    "hex": hexRegex,
    "str": "[\s\S]*"
}

colorDict: dict = {
    "COLOR_NAME": "[A-z]+",
    "OPACITY": floatRegex,
}

rotationDict: dict = {
    "X": floatRegex,
    "Y": floatRegex,
    "Z": floatRegex,
    "DEGREES": floatRegex,
        "ROTATION_VECTOR": {
            "X": floatRegex,
            "Y": floatRegex,
            "Z": floatRegex
        }
}

positionDict: dict = {
    "X": floatRegex,
    "Y": floatRegex,
    "Z": floatRegex
}

tokens: dict = {
    "LET": {
        "BODY": {
            varNameRegex: {
                "CUBE": {
                    "SIDE": floatRegex,
                    "SIZE": positionDict,
                    "POSITION": positionDict,
                    "ROTATION": rotationDict,
                    "CENTER": boolRegex,
                    "COLOR": colorDict,
                    "COLOR_HEX": hexRegex
                },
                "SPHERE": {
                    "RADIUS": floatRegex,
                    "DIAMETER": floatRegex,
                    "POSITION": positionDict,
                    "FRAGMENTS_ANGLE": floatRegex,
                    "FRAGMENTS_SIZE": floatRegex,
                    "RESOLUTION": floatRegex,
                    "ROTATION": rotationDict,
                    "COLOR": colorDict,
                    "COLOR_HEX": hexRegex
                },
                "CYLINDER": {
                    "RADIUS": floatRegex,
                    "DIAMETER": floatRegex,
                    "RADIUS_BOTTOM": floatRegex,
                    "RADIUS_TOP": floatRegex,
                    "DIAMETER_BOTTOM": floatRegex,
                    "DIAMETER_TOP": floatRegex,
                    "POSITION": positionDict,
                    "CENTER": boolRegex,
                    "FRAGMENTS_ANGLE": floatRegex,
                    "FRAGMENTS_SIZE": floatRegex,
                    "RESOLUTION": floatRegex,
                    "ROTATION": rotationDict,
                    "COLOR": colorDict,
                    "COLOR_HEX": hexRegex
                },
                "ENCIRCLEMENT": {
                    "POSITION": positionDict,
                    "OBJECT": varNameRegex,
                    "WITH": varNameRegex,
                    "AMOUNT": intRegex,
                    "OFFSET_ANGLE": floatRegex,
                    "OFFSET_COUNT": floatRegex
                }
            }
        },
        "int": intRegex,
        "float": floatRegex,
        "bool": boolRegex,
        "str": "[\s\S]*",
        "CONSTANT": {
                varNameRegex: primitiveDict
            }
    },
    "PLACE": {
        "OBJECT": varNameRegex,
        "X": floatRegex,
        "Y": floatRegex,
        "Z": floatRegex
    },
    "MOVE": {
        "OBJECT": varNameRegex,
        "X": floatRegex,
        "Y": floatRegex,
        "Z": floatRegex
    },
    "ROTATE": {
        "OBJECT": varNameRegex,
        "X": floatRegex,
        "Y": floatRegex,
        "Z": floatRegex,
        "DEGREES": floatRegex,
        "ROTATION_VECTOR": {
            "X": floatRegex,
            "Y": floatRegex,
            "Z": floatRegex
        }
    },
    "SURROUND": {
        "OBJECT": varNameRegex,
        "WITH": varNameRegex,
        "X": floatRegex,
        "Y": floatRegex,
        "Z": floatRegex,
        "AMOUNT": floatRegex,
        "OFFSET_ANGLE": floatRegex,
        "OFFSET_COUNT": floatRegex
    }
}

class LexicalAnalyser:
    def __init__(self) -> None:
        self.comment_regex: str = "(/\*[\s\S]*?\*/)|(\/\/.*)"
        self.code: str = str()
        self.commands: list = list()

    def extract_source(self, source: str="source.chimera") -> None:
        with open(source, 'r') as file:
            contents: str = file.read()
            file.close()
        
        comments = re.findall(self.comment_regex, contents)
        for match in comments:
            for group in match:
                contents = contents.replace(group, "")
        self.code = contents

    # Replaces multiple spaces with single spaces, then separates the code by semicolons
    # and, at last, makes nested lists by separating further by spaces, as well as 
    # filtering out the empty strings
    def extract_commands(self) -> None:
        if len(self.code) == 0:
            raise RuntimeError("Nothing to extract, code is empty")
        else:
            commands = re.sub("\s+", " ", self.code).split(";")
            self.commands = [list(filter(None, i.split(" "))) for i in commands]
    
    # def tokenize(self) -> None:

    # def lexical_analysis(self, sorce: str="source.chimera")

class VAR:
    def __init__(self, is_const: bool, vType: type, name: str, value) -> None:
        self.is_const = is_const
        self.vType = type
        self.name = name
        self.value = value
    
    def __add__(self, VAR):
        return self.value + VAR.value
    
    def __mul__(self, VAR):
        return self.value * VAR.value

    def le__(self, value):
        return self.value <= value
        
    def __pow__(self, value, mod):
        return pow(self.value, value, mod)
        
    def __lt__(self, value):
        return self.value < value
        
    def __mod__(self, value):
        return self.value % value

class BODY:
    def __init__(self,
                POSITION=[0, 0, 0],
                ROTATION=[0, 0, 0, 0, [0, 0, 0]],
                COLOR=["", 1, 0XFF_FF_FF]
                ) -> None:

        self.POSITION = {
            "X": POSITION[0],
            "Y": POSITION[1],
            "Z": POSITION[2]
        }

        self.ROTATION = {
            "X": ROTATION[0],
            "Y": ROTATION[1],
            "Z": ROTATION[2],
            "DEGREES": ROTATION[3],
            "ROTATION VECTOR": {
                "X": ROTATION[4][0],
                "Y": ROTATION[4][1],
                "Z": ROTATION[4][2]
            }
        }

        self.COLOR = {
            "COLOR_NAME": COLOR[0],
            "OPACITY": COLOR[1]
        }

        self.COLOR_HEX = COLOR[2]

class CUBE(BODY):
    def __init__(self,
                POSITION=[0, 0, 0],
                ROTATION=[0, 0, 0, 0, [0, 0, 0]],
                COLOR=["", 1, 0XFF_FF_FF],
                SIDE = 0,
                SIZE = [0, 0, 0],
                CENTER = True
                ) -> None:

        super().__init__(self, POSITION=POSITION, ROTATION=ROTATION, COLOR=COLOR)

        self.SIDE = SIDE,
        self.SIZE = {
            "X": SIZE[0],
            "Y": SIZE[1],
            "Z": SIZE[2]
        }
        
        self.CENTER = CENTER

class SPHERE(BODY):
    def __init__(self,
                POSITION=[0, 0, 0],
                ROTATION=[0, 0, 0, 0, [0, 0, 0]],
                COLOR=["", 1, 0XFF_FF_FF],
                RADIUS = 0,
                DIAMETER = 0,
                FRAGMENTS_ANGLE = 0,
                FRAGMENTS_SIZE = 0,
                RESOLUTION = 0
                ) -> None:

        super().__init__(self, POSITION=POSITION, ROTATION=ROTATION, COLOR=COLOR)

        self.RADIUS = RADIUS
        self.DIAMETER = DIAMETER

        self.FRAGMENTS_ANGLE = FRAGMENTS_ANGLE
        self.FRAGMENTS_SIZE = FRAGMENTS_SIZE
        self.RESOLUTION = RESOLUTION

class CYLINDER(SPHERE):
    def __init__(self,
                POSITION=[0, 0, 0],
                ROTATION=[0, 0, 0, 0, [0, 0, 0]],
                COLOR=["", 1, 0XFF_FF_FF],
                RADIUS = 0,
                DIAMETER = 0,
                FRAGMENTS_ANGLE = 0,
                FRAGMENTS_SIZE = 0,
                RESOLUTION = 0,
                RADIUS_BOTTOM = 0,
                RADIUS_TOP = 0,
                DIAMETER_BOTTOM = 0,
                DIAMETER_TOP = 0
                ) -> None:

        super().__init__(self, POSITION=POSITION, ROTATION=ROTATION, COLOR=COLOR,
        RADIUS=RADIUS, DIAMETER=DIAMETER, FRAGMENTS_ANGLE=FRAGMENTS_ANGLE,
        FRAGMENTS_SIZE=FRAGMENTS_SIZE, RESOLUTION=RESOLUTION)

        self.RADIUS_BOTTOM = RADIUS_BOTTOM
        self.RADIUS_TOP = RADIUS_TOP
        self.DIAMETER_BOTTOM = DIAMETER_BOTTOM
        self.DIAMETER_TOP = DIAMETER_TOP

class ENCIRCLEMENT:
    def __init__(self,
                OBJECT=None,
                WITH=None,
                AMOUNT=0,
                OFFSET_ANGLE=0,
                OFFSET_COUNT=0
                ) -> None:
                
        self.OBJECT = OBJECT
        self.WITH = WITH
        self.AMOUNT = AMOUNT
        self.OFFSET_ANGLE = OFFSET_ANGLE
        self.OFFSET_COUNT = OFFSET_COUNT

class OP:
    def __init__(self, OBJECT: BODY, X: float, Y: float, Z: float) -> None:
        self.OBJECT = OBJECT
        self.X = X
        self.Y = Y
        self.Z = Z

class PLACE(OP):
    def __init__(self, OBJECT: BODY, X: float, Y: float, Z: float) -> None:
        super().__init__(OBJECT, X, Y, Z)

class MOVE(OP):
    def __init__(self,
                OBJECT: BODY,
                X: float,
                Y: float,
                Z: float
                ) -> None:

        super().__init__(OBJECT, X, Y, Z)

class ROTATE(OP):
    def __init__(self,
                OBJECT: BODY,
                X: float,
                Y: float,
                Z: float,
                DEGREES: float,
                ROTATION_VECTOR: list
                ) -> None:

        super().__init__(OBJECT, X, Y, Z)
        DEGREES = DEGREES
        ROTATION_VECTOR = ROTATION_VECTOR

class SURROUND(OP):
    def __init__(self,
                OBJECT: BODY,
                X: float,
                Y: float,
                Z: float,
                WITH: BODY,
                AMOUNT: int,
                OFFSET_ANGLE: float,
                OFFSET_COUNT: float,
                ) -> None:

        super().__init__(OBJECT, X, Y, Z)
        self.WITH = WITH
        self.AMOUNT = AMOUNT
        self.OFFSET_ANGLE = OFFSET_ANGLE
        self.OFFSET_COUNT = OFFSET_COUNT

def to_or_regex(args: list) -> str:
    string = "|".join(args)
    regex = f"({string})"
    return regex

# types: str = to_or_regex(type_list)
# variable_regex: str = f"(LET|CONSTANT)\s+{types}\s+([A-z][A-z0-9]*)\s+=\s([\s\S]*?);"

# bodies: str = to_or_regex(body_list)
# body_regex: str = f"(BODY)\s+([A-z][A-z0-9]*)\s+=\s+{bodies}([\s\S]*?);"

# plain_arg_regex: str = "([A-z]+)\s+=\s+([A-z0-9\.]+),?"
# nested_arg_regex: str = "([A-z]+)\s+=\s*\{([\s\S]*?)\},?"

if __name__ == '__main__':
    pass