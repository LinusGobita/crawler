from enum import Enum


class ListerType(Enum):
    AGENCY = "AGENCY"


class Lister:

    def __init__(self, lister_id:str, lister_name: str, lister_type: ListerType):
        self.lister_id = lister_id
        self.lister_name = lister_name
        if lister_type not in ListerType:
            print(f"ERROR: Type '{lister_type} not known!")
            exit(1)
        self.lister_type = lister_type.value
