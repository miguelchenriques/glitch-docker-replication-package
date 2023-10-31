import csv
from dataclasses import astuple, dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Smell:
    file: str
    smell: Optional[str]
    line: int
    code: Optional[str] = None

    def __iter__(self):
        return iter(astuple(self))

    @staticmethod
    def load_smell_csv(file_path: Path) -> Dict[str, List["Smell"]]:
        smells: Dict[str, List[Smell]] = {}
        with open(file_path) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                file_name, smell, line = row
                if not smells.get(file_name):
                    smells[file_name] = []
                smells[file_name].append(Smell(file_name, smell, int(line) if line else 0))
        return smells


smell_mapper = {
    "SM01": "sec_def_admin",
    "SM02": "sec_empty_pass",
    "SM03": "sec_hard_secr", # Complexo
    "SM04": "sec_invalid_bind",
    "SM05": "sec_susp_comm",
    "SM06": "sec_https",
    "SM07": "sec_weak_crypt",
    "SM08": "sec_full_permission_filesystem",
    "SM09": "sec_non_official_image",
    "SM10": "sec_obsolete_command",
    "SM11": "sec_no_int_check",
}
