import json
from typing import Any, TypedDict, cast
from typing_extensions import ReadOnly


class CaseForms(TypedDict):
    nominative: ReadOnly[str]
    genitive: ReadOnly[str]
    dative: ReadOnly[str]
    accusative: ReadOnly[str]
    locative: ReadOnly[str]
    instrumental: ReadOnly[str]


class Pattern(TypedDict):
    singular: ReadOnly[CaseForms]
    plural: ReadOnly[CaseForms]


def validate_pattern(pattern: Any) -> Pattern:
    """Validate the shape of the given pattern."""

    if not isinstance(pattern, dict):
        raise ValueError(
            f"Expected each pattern to be {dict}, but received "
            f"{type(pattern)} in pattern {pattern}"
        )
    NUMBER_KEYS = {'singular', 'plural'}
    if set(pattern.keys()) != NUMBER_KEYS:
        raise ValueError(
            f"Expected each pattern to have the keys {sorted(NUMBER_KEYS)}, "
            f"but received {sorted(pattern.keys())} in pattern {pattern}"
        )

    CASE_NAMES = {
        'nominative',
        'genitive',
        'dative',
        'accusative',
        'locative',
        'instrumental',
    }
    for number in NUMBER_KEYS:
        cases = pattern[number]

        if not isinstance(cases, dict):
            raise ValueError(
                f"Expected {sorted(NUMBER_KEYS)} keys in each pattern to map "
                f"to {dict}, but {number} is mapped to {type(cases)} in "
                f"pattern {pattern}"
            )
        if set(cases.keys()) != CASE_NAMES:
            raise ValueError(
                f"Expected keys for {number} number are {sorted(CASE_NAMES)}, "
                f"but received {sorted(cases.keys())} in pattern {pattern}"
            )

        if not all(isinstance(value, str) for value in cases.values()):
            raise ValueError(
                f"Expected each declension pattern value to be of {str}, but "
                f"received {cases.values()}."
            )

    return cast(Pattern, pattern)


def load_patterns(
    file_name: str = 'slovak_declension_patterns.jsonl',
) -> list[Pattern]:
    """Load and return all declension pattern found in the given file."""

    patterns: list[Pattern] = []
    with open(file_name, mode='r') as f:
        for pattern_str in f.readlines():
            pattern = validate_pattern(json.loads(pattern_str))
            patterns.append(pattern)

    return patterns


def main():
    patterns = load_patterns()


if __name__ == '__main__':
    main()
