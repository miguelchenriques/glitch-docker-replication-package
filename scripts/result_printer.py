from typing import Dict
from tabulate import tabulate
from scripts.smell.smell_occurance import SmellOccurrance
from scripts.smell.smell import smell_mapper


def print_oracle_table(smell_occurrances: Dict[str, SmellOccurrance]):
    headers = ["Smell", "Occurrances", "Detected", "Accuracy", "Recall"]
    data = []
    for smell, occurance in smell_occurrances.items():
        total_detections = occurance.correct_detection +\
                occurance.incorrect_detection
        accuracy = occurance.correct_detection / total_detections \
            if total_detections > 0 else 0
        recall = occurance.correct_detection / occurance.occurance \
            if occurance.occurance > 0 else 0
        data.append([
            smell,
            occurance.occurance,
            total_detections,
            round(accuracy, 2),
            round(recall, 2)
            ])
    print(tabulate(data, headers=headers))


def print_dataset_results(smells: dict, files: int, loc: int):
    results = {smell: {'occurrances': 0, 'files': 0} for smell in smell_mapper.values()}
    for smell in smells:
        results[smell['code']]['occurrances'] += 1

    afected_files = {smell: 0 for smell in smell_mapper.values()}
    for smell, result in results.items():
        result['files'] = len(set(s['file'] for s in smells if s['code'] == smell))

    headers = ["Smell", "Ocurrances", "Smell per KLOC", "Script%"]
    data = []
    for smell, result in results.items():
        data.append(
                [
                    smell,
                    result['occurrances'],
                    round(result['occurrances'] / loc * 1000, 2),
                    round(result['files'] / files * 100, 2),
                    ]
                )
    total_occurrances = len(smells)
    total_affected_files = len(set(s['file'] for s in smells))
    data.append(
            [
                "Total",
                total_occurrances,
                round(total_occurrances / loc * 1000, 2),
                round(total_affected_files / files * 100, 2),
                ]
            )
    print(tabulate(data, headers=headers))

    print(tabulate([[files, loc]], headers=["Total IaC files", "Lines of code"]))
