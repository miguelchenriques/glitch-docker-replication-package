import sys
from typing import Dict
from scripts.smell.smell import smell_mapper, Smell
from scripts.smell.smell_occurance import SmellOccurrance
from scripts.result_printer import print_oracle_table, print_dataset_results
from pathlib import Path
from tqdm import tqdm
from dsl.core.rules.Engine import Engine
from dsl.core.analysis.lexical.LexicalAnalysis import LexicalAnalysis

root_folder = Path().absolute()
datasets = root_folder / 'datasets'


def analyze_oracle() -> None:
    existing_smells = Smell.load_smell_csv(datasets / 'oracle-classification.csv')
    results: Dict[str, SmellOccurrance] = {
            smell: SmellOccurrance() for smell in smell_mapper.values()
            }

    dockerfiles_path = datasets / 'docker-oracle'
    incorrect_detections = []
    for path in tqdm(dockerfiles_path.iterdir()):
        smells = get_dockerfile_smells(path)

        correct = []
        incorrect = []
        file_smells = existing_smells.get(path.name, [])
        for smell in smells:
            if smell['code'] == 'sec_def_admin' and any(
                    s.smell == 'sec_def_admin' for s in file_smells):
                correct.append(smell)
                continue
            if any(
                    smell['code'] == s.smell and
                    s.line >= smell['start_line'] and
                    s.line <= smell['end_line']
                    for s in file_smells
                    ):
                correct.append(smell)
                continue
            incorrect.append(smell)

        incorrect_detections += incorrect

        for smell in file_smells:
            results[smell.smell].occurance += 1
        for smell in correct:
            results[smell['code']].correct_detection += 1
        for smell in incorrect:
            results[smell['code']].incorrect_detection += 1

    print_oracle_table(results)


def get_dockerfile_smells(file: Path) -> list:
    try:
        dockerfile_content = file.read_text()
        lexical = LexicalAnalysis(dockerfile_content)
        lexical.parse()
        tokens = lexical.get_tokens()
        smells = Engine(tokens).run()
        for smell in smells:
            smell['code'] = smell_mapper[smell['code']]
            smell['file'] = file.name
        return smells
    except:
        return []


def analyze_dataset():
    dataset = datasets / 'docker'

    smells = []
    lines = 0
    for file in tqdm(dataset.iterdir()):
        smells += get_dockerfile_smells(file)
        with open(file) as f:
            lines += len(f.readlines())

    print_dataset_results(smells, len(list(dataset.iterdir())), lines)


if __name__ == '__main__':
    choice = sys.argv[1]
    if choice == 'oracle':
        analyze_oracle()
    if choice == 'dataset':
        analyze_dataset()
