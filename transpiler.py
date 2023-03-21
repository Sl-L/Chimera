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
                POSITION: dict ={'X': 0, 'Y': 0, 'Z': 0},
                ROTATION: dict ={'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                COLOR: dict ={'COLOR_NAME': "", 'OPACITY': 1},
                COLOR_HEX: int = 0
                ) -> None:

        self.POSITION: list = {
            "X": POSITION['X'],
            "Y": POSITION['Y'],
            "Z": POSITION['Z']
        }

        self.ROTATION: dict = {
            "X": ROTATION['X'],
            "Y": ROTATION['Y'],
            "Z": ROTATION['Z'],
            "DEGREES": ROTATION['DEGREES'],
            "ROTATION_VECTOR": {
                "X": ROTATION['ROTATION_VECTOR']['X'],
                "Y": ROTATION['ROTATION_VECTOR']['Y'],
                "Z": ROTATION['ROTATION_VECTOR']['Z']
            }
        }

        self.COLOR: dict = {
            "COLOR_NAME": COLOR['COLOR_NAME'],
            "OPACITY": COLOR['OPACITY']
        }

        self.COLOR_HEX: int = COLOR_HEX

class CUBE(BODY):
    def __init__(self,
                POSITION: list ={'X': 0, 'Y': 0, 'Z': 0},
                ROTATION: dict ={'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                COLOR: list ={'COLOR_NAME': "", 'OPACITY': 1},
                SIDE: float = 0,
                SIZE: list = {'X': 0, 'Y': 0, 'Z': 0},
                CENTER: bool = True,
                COLOR_HEX: int = True
                ) -> None:

        super().__init__(POSITION=POSITION, ROTATION=ROTATION, COLOR=COLOR, COLOR_HEX=COLOR_HEX)

        self.SIDE: float = SIDE,
        self.SIZE: list = {
            "X": SIZE['X'],
            "Y": SIZE['Y'],
            "Z": SIZE['Z']
        }
        
        self.CENTER: bool = CENTER

class SPHERE(BODY):
    def __init__(self,
                POSITION: list ={'X': 0, 'Y': 0, 'Z': 0},
                ROTATION: dict ={'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                COLOR: list ={'COLOR_NAME': "", 'OPACITY': 1},
                RADIUS: float = 0,
                DIAMETER: float = 0,
                FRAGMENTS_ANGLE: float = 0,
                FRAGMENTS_SIZE: float = 0,
                RESOLUTION: int = 0,
                COLOR_HEX: int = True
                ) -> None:

        super().__init__(self, POSITION=POSITION, ROTATION=ROTATION, COLOR=COLOR, COLOR_HEX=COLOR_HEX)

        self.RADIUS: float = RADIUS
        self.DIAMETER: float = DIAMETER

        self.FRAGMENTS_ANGLE: float = FRAGMENTS_ANGLE
        self.FRAGMENTS_SIZE: float = FRAGMENTS_SIZE
        self.RESOLUTION: int = RESOLUTION

class CYLINDER(SPHERE):
    def __init__(self,
                POSITION: list ={'X': 0, 'Y': 0, 'Z': 0},
                ROTATION: dict ={'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                COLOR: list ={'COLOR_NAME': "", 'OPACITY': 1},
                RADIUS: float = 0,
                DIAMETER: float = 0,
                FRAGMENTS_ANGLE: float = 0,
                FRAGMENTS_SIZE: float = 0,
                RESOLUTION: float = 0,
                RADIUS_BOTTOM: float = 0,
                RADIUS_TOP: float = 0,
                DIAMETER_BOTTOM: float = 0,
                DIAMETER_TOP: float = 0,
                COLOR_HEX: int = True
                ) -> None:

        super().__init__(self, POSITION=POSITION, ROTATION=ROTATION, COLOR=COLOR,
        RADIUS=RADIUS, DIAMETER=DIAMETER, FRAGMENTS_ANGLE=FRAGMENTS_ANGLE,
        FRAGMENTS_SIZE=FRAGMENTS_SIZE, RESOLUTION=RESOLUTION, COLOR_HEX=COLOR_HEX)

        self.RADIUS_BOTTOM: float = RADIUS_BOTTOM
        self.RADIUS_TOP: float = RADIUS_TOP
        self.DIAMETER_BOTTOM: float = DIAMETER_BOTTOM
        self.DIAMETER_TOP: float = DIAMETER_TOP

class ENCIRCLEMENT:
    def __init__(self,
                OBJECT=None,
                WITH=None,
                AMOUNT: int =0,
                OFFSET_ANGLE: float =0,
                OFFSET_COUNT: float =0
                ) -> None:
                
        self.OBJECT = OBJECT
        self.WITH = WITH
        self.AMOUNT: int = AMOUNT
        self.OFFSET_ANGLE: float = OFFSET_ANGLE
        self.OFFSET_COUNT: float = OFFSET_COUNT

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
                ROTATION_VECTOR: dict
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
                TARGET: BODY,
                AMOUNT: int,
                OFFSET_ANGLE: float,
                OFFSET_COUNT: float,
                ) -> None:

        super().__init__(OBJECT, X, Y, Z)
        self.TARGET = TARGET
        self.AMOUNT = AMOUNT
        self.OFFSET_ANGLE = OFFSET_ANGLE
        self.OFFSET_COUNT = OFFSET_COUNT

class LexicalAnalyser:
    def __init__(self) -> None:
        self.comment_regex: str = "(/\*[\s\S]*?\*/)|(\/\/.*)"
        self.code: str = str()
        self.commands: list = list()
        self.ops: list = [[]]

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
            commands = re.sub("[\s\)]+", " ", self.code).split(";")
            commands = [i.split("(") for i in commands]
            commands = [
                    list(filter(None, i[0].split(" ")))
                if len(i) == 1
                else
                    [
                        list(filter(None, i[0].split(" "))),
                        eval("{{ {0} }}".format(re.sub(r"\b([A-z][A-z0-9]*)", r"'\1'", i[1]).replace("\"'", "'").replace("'\"", "'").replace("=", ":")))
                    ]
                for i in commands]

            self.commands = commands

    def verify_commands(self):
        for index, i in enumerate(self.commands):
            if len(i) == 0:
                continue
            elif type(i[0]) == str:
                if i[0] not in {"CONSTANT", "LET"}:
                    raise(SyntaxError(f"Unknown keyword '{i[0]}'"))

                const = False
                if len(i) != 5:
                    raise(TypeError(f"Expected exactly 5 arguments, got {len(i)}"))
                if i[0] == "CONSTANT":
                    const = True
                
                self.ops.append([index, i[2], VAR(const, i[1], i[2], i[3])])
            elif type(i[0] == list):
                if i[0][0] in {"PLACE", "MOVE", "ROTATE", "SURROUND"}:
                    if 'OBJECT' not in i[1]:
                        raise(TypeError(f"Argument 'OBJECT' missing for {i[0][0]} operation"))

                    if i[0][0] == "PLACE":
                        self.ops.append([index, PLACE(
                            OBJECT=i[1]['OBJECT'],
                            X= i[1]['X'] if 'X' in i[1].keys() else 0,
                            Y= i[1]['Y'] if 'Y' in i[1].keys() else 0,
                            Z= i[1]['Z'] if 'Z' in i[1].keys() else 0)
                            ])

                    elif i[0][0] == "MOVE":
                        self.ops.append([index, MOVE(
                            OBJECT=i[1]['OBJECT'],
                            X= i[1]['X'] if 'X' in i[1].keys() else 0,
                            Y= i[1]['Y'] if 'Y' in i[1].keys() else 0,
                            Z= i[1]['Z'] if 'Z' in i[1].keys() else 0)
                            ])
                    
                    elif i[0][0] == "ROTATE":
                        self.ops.append([index, ROTATE(
                            OBJECT=i[1]['OBJECT'],
                            X= i[1]['X'] if 'X' in i[1].keys() else 0,
                            Y= i[1]['Y'] if 'Y' in i[1].keys() else 0,
                            Z= i[1]['Z'] if 'Z' in i[1].keys() else 0,
                            DEGREES= i[1]['DEGREES'] if 'DEGREES' in i[1].keys() else 0,
                            ROTATION_VECTOR= i[1]['ROTATION_VECTOR'] if 'ROTATION_VECTOR' in i[1].keys() else 0)
                            ])

                    elif i[0][0] == "SURROUND":
                        self.ops.append([index, SURROUND(
                            OBJECT=i[1]['OBJECT'],
                            X= i[1]['X'] if 'X' in i[1].keys() else 0,
                            Y= i[1]['Y'] if 'Y' in i[1].keys() else 0,
                            Z= i[1]['Z'] if 'Z' in i[1].keys() else 0,
                            TARGET= i[1]['TARGET'] if 'TARGET' in i[1].keys() else 0,
                            AMOUNT= i[1]['AMOUNT'] if 'AMOUNT' in i[1].keys() else 0,
                            OFFSET_ANGLE= i[1]['OFFSET_ANGLE'] if 'OFFSET_ANGLE' in i[1].keys() else 0,
                            OFFSET_COUNT= i[1]['OFFSET_COUNT'] if 'OFFSET_COUNT' in i[1].keys() else 0)
                            ])

                    else:
                        raise(TypeError("This shouldn't had happened, like... how?"))

                elif i[0][4] in {"CUBE", "SPHERE", "CYLINDER", "ENCIRCLEMENT"}:
                    if i[0][4] == "CUBE":
                        self.ops.append([index, i[0][2], CUBE(
                            POSITION= i[1]["POSITION"] if 'POSITION' in i[1].keys() else {'X': 0, 'Y': 0, 'Z': 0},
                            ROTATION= i[1]["ROTATION"] if 'ROTATION' in i[1].keys() else {'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                            COLOR= i[1]["COLOR"] if 'COLOR' in i[1].keys() else {'COLOR_NAME': "", 'OPACITY': 1},
                            SIDE= i[1]["SIDE"] if 'SIDE' in i[1].keys() else 1,
                            SIZE= i[1]["SIZE"] if 'SIZE' in i[1].keys() else {'X': 0, 'Y': 0, 'Z': 0},
                            CENTER= i[1]["CENTER"] if 'CENTER' in i[1].keys() else True
                        )])

                    elif i[0][4] == "SPHERE":
                        self.ops.append([index, i[0][2], SPHERE(
                            POSITION= i[1]["POSITION"] if 'POSITION' in i[1].keys() else {'X': 0, 'Y': 0, 'Z': 0},
                            ROTATION= i[1]["ROTATION"] if 'ROTATION' in i[1].keys() else {'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                            COLOR= i[1]["COLOR"] if 'COLOR' in i[1].keys() else {'COLOR_NAME': "", 'OPACITY': 1},
                            RADIUS= i[1]["RADIUS"] if 'RADIUS' in i[1].keys() else 0.5,
                            DIAMETER= i[1]["DIAMETER"] if 'DIAMETER' in i[1].keys() else 1,
                            FRAGMENTS_ANGLE= i[1]["FRAGMENTS_ANGLE"] if 'FRAGMENTS_ANGLE' in i[1].keys() else 1,
                            FRAGMENTS_SIZE= i[1]["FRAGMENTS_SIZE"] if 'FRAGMENTS_SIZE' in i[1].keys() else 1,
                            RESOLUTION= i[1]["RESOLUTION"] if 'RESOLUTION' in i[1].keys() else 300
                        )])

                    elif i[0][4] == "CYLINDER":
                        self.ops.append([index, i[0][2], CYLINDER(
                            POSITION= i[1]["POSITION"] if 'POSITION' in i[1].keys() else {'X': 0, 'Y': 0, 'Z': 0},
                            ROTATION= i[1]["ROTATION"] if 'ROTATION' in i[1].keys() else {'X': 0, 'Y': 1, 'Z': 0, 'DEGREES': 0, 'ROTATION_VECTOR': {'X': 0, 'Y': 0, 'Z': 0}},
                            COLOR= i[1]["COLOR"] if 'COLOR' in i[1].keys() else {'COLOR_NAME': "", 'OPACITY': 1},
                            RADIUS= i[1]["RADIUS"] if 'RADIUS' in i[1].keys() else 0.5,
                            RADIUS_TOP= i[1]["RADIUS_TOP"] if 'RADIUS' in i[1].keys() else 0.5,
                            RADIUS_BOTTOM= i[1]["RADIUS_BOTTOM"] if 'RADIUS' in i[1].keys() else 0.5,
                            DIAMETER= i[1]["DIAMETER"] if 'DIAMETER' in i[1].keys() else 1,
                            DIAMETER_TOP= i[1]["DIAMETER_TOP"] if 'DIAMETER' in i[1].keys() else 1,
                            DIAMETER_BOTTOM= i[1]["DIAMETER_BOTTOM"] if 'DIAMETER' in i[1].keys() else 1,
                            FRAGMENTS_ANGLE= i[1]["FRAGMENTS_ANGLE"] if 'FRAGMENTS_ANGLE' in i[1].keys() else 1,
                            FRAGMENTS_SIZE= i[1]["FRAGMENTS_SIZE"] if 'FRAGMENTS_SIZE' in i[1].keys() else 1,
                            RESOLUTION= i[1]["RESOLUTION"] if 'RESOLUTION' in i[1].keys() else 300
                        )])

                    elif i[0][4] == "ENCIRCLEMENT":
                        self.ops.append([index, i[0][2], ENCIRCLEMENT(
                            OBJECT= i[1]["OBJECT"] if 'OBJECT' in i[1].keys() else None,
                            WITH= i[1]["WITH"] if 'WITH' in i[1].keys() else None,
                            AMOUNT= i[1]["AMOUNT"] if 'AMOUNT' in i[1].keys() else 0,
                            OFFSET_ANGLE= i[1]["OFFSET_ANGLE"] if 'OFFSET_ANGLE' in i[1].keys() else 0,
                            OFFSET_COUNT= i[1]["OFFSET_COUNT"] if 'OFFSET_COUNT' in i[1].keys() else 0,
                        )])

                    else:
                        raise(TypeError("This shouldn't had happened, like... how? (2)"))



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
    a = LexicalAnalyser()
    a.extract_source()
    a.extract_commands()
    a.verify_commands()
    for i in a.ops:
        print(i)