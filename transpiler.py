import re

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

def to_or_regex(args: list) -> str:
    string = "|".join(args)
    regex = f"({string})"
    return regex

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

types = to_or_regex(type_list)
variable_regex = f"(LET|CONSTANT)\s+{types}\s+([A-z][A-z0-9]*)\s+=\s([\s\S]*?);"

bodies = to_or_regex(body_list)
body_regex = f"(BODY)\s+([A-z][A-z0-9]*)\s+=\s+{bodies}([\s\S]*?);"

comment_regex = "(/\*[\s\S]*?\*/)|(\/\/.*)"

if __name__ == '__main__':
    with open('source.chimera', 'r') as file:
        contents: str = file.read()
        file.close()
    
    comments = re.findall(comment_regex, contents)
    for match in comments:
        for group in match:
            contents = contents.replace(group, "")
    
    [print(i) for i in re.findall(variable_regex, contents)]
    [print(i) for i in re.findall(body_regex, contents)]