import re

commands_list: list = [
    "LET",
    "CONSTANT",
    "BODY",
    "MOVE",
    "ROTATE",
    "SURROUND"
]

body_list: list = [
    "CUBE",
    "SPHERE",
    "CYLINDER",
    "ENCIRCLEMENT"
]

type_list: list = [
    "int",
    "float",
    "str",
    "bool"
]

"""
 nType can be:
    - "VAR"
        - "constant"
        - "mutable"
        - "type"
        - "name"
        - "value"
    - "BODY"
        - "CUBE"
        - "SPHERE"
        - "CYLINDER"
        - "ENCIRCLEMENT"
    - "OP"
        - "PLACE"
        - "MOVE"
        - "ROTATE"
        - "SURROUND"
"""
class Node:
    def __init__(self, id: int, nType: str) -> None:
        self.id = id
        self.nType = nType

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
                CENTER: bool
                ) -> None:

        super().__init__(OBJECT, X, Y, Z)
        self.WITH = WITH
        self.AMOUNT = AMOUNT
        self.OFFSET_ANGLE = OFFSET_ANGLE
        self.OFFSET_COUNT = OFFSET_COUNT
        self.CENTER = CENTER

def to_or_regex(args: list) -> str:
    string = "|".join(args)
    regex = f"({string})"
    return regex

types: str = to_or_regex(type_list)
variable_regex: str = f"(LET|CONSTANT)\s+{types}\s+([A-z][A-z0-9]*)\s+=\s([\s\S]*?);"

bodies: str = to_or_regex(body_list)
body_regex: str = f"(BODY)\s+([A-z][A-z0-9]*)\s+=\s+{bodies}([\s\S]*?);"

plain_arg_regex: str = "([A-z]+)\s+=\s+([A-z0-9\.]+),?"
nested_arg_regex: str = "([A-z]+)\s+=\s*\{([\s\S]*?)\},?"

comment_regex: str = "(/\*[\s\S]*?\*/)|(\/\/.*)"

if __name__ == '__main__':
    with open('source.chimera', 'r') as file:
        contents: str = file.read()
        file.close()
    
    comments = re.findall(comment_regex, contents)
    for match in comments:
        for group in match:
            contents = contents.replace(group, "")
    
    v = re.findall(variable_regex, contents)
    b = re.findall(body_regex, contents)

    print(b)
    print(v)

