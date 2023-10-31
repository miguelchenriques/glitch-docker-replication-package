import os
from tqdm import tqdm
from pathlib import Path
from typing import Dict, List
from glitch.parsers.docker_parser import DockerParser
from glitch.repr.inter import UnitBlockType
from glitch.tech import Tech
from glitch.analysis.security import SecurityVisitor
from scripts.smell.smell import Smell, smell_mapper
from scripts.smell.smell_occurance import SmellOccurrance
from scripts.result_printer import print_oracle_table
from pkg_resources import resource_filename
from glitch.analysis.rules import Error


root_folder = Path().absolute()
datasets = root_folder / 'datasets'
dockerfiles_path = datasets / 'docker-oracle'


SmellName = str
results: Dict[SmellName, SmellOccurrance] = {
        smell: SmellOccurrance() for smell in smell_mapper.values()}
incorrect: List[Error] = []
missed: List[Smell] = []


def load_smell_code(file_smells: Dict[str, List[Smell]]):
    for file, smells in file_smells.items():
        path = dockerfiles_path / file
        lines = read_file_lines(path)
        for smell in smells:
            if smell.smell is None:
                continue
            smell.code = lines[smell.line]


def read_file_lines(file: Path) -> Dict[int, str]:
    lines = {}
    with open(file) as f:
        for i, line in enumerate(f):
            lines[i] = line.strip()
    return lines


def get_dockerfile_sec_smells(file: Path) -> List[Error]:
    inter = DockerParser().parse(file, UnitBlockType.script, False)
    analyzer = SecurityVisitor(Tech.docker)
    config = resource_filename('glitch', "configs/default.ini")
    analyzer.config(config)
    errors = analyzer.check(inter)

    return [e for e in errors if e.code in smell_mapper.values()]


def analyze_oracle() -> None:
    existing_smells = Smell.load_smell_csv(datasets / 'oracle-classification.csv')
    load_smell_code(existing_smells)
    results: Dict[str, SmellOccurrance] = {
            smell: SmellOccurrance() for smell in smell_mapper.values()}
    incorrect: List[Error] = []

    for path in tqdm(dockerfiles_path.iterdir()):
        file_smells = existing_smells.get(path.name, [])
        errors = get_dockerfile_sec_smells(path)
        correct_detections = []
        incorrect_detections = []

        for error in errors:
            same_smell_code = [s for s in file_smells if s.smell == error.code]

            if any(
                    s.line == error.line or
                    s.code in error.el.code
                    for s in same_smell_code):
                correct_detections.append(error)
            else:
                incorrect_detections.append(error)

        incorrect += incorrect_detections

        for smell in file_smells:
            results[smell.smell].occurance += 1
        for error in correct_detections:
            results[error.code].correct_detection += 1
        for error in incorrect_detections:
            results[error.code].incorrect_detection += 1

    print_oracle_table(results)


if __name__ == '__main__':
    analyze_oracle()
