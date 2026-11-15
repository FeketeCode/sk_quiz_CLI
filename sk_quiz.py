import pprint
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


NUMBER_KEYS = ('singular', 'plural')
CASE_NAMES = (
    'nominative',
    'genitive',
    'dative',
    'accusative',
    'locative',
    'instrumental',
)


def validate_pattern(pattern: Any) -> Pattern:
    """Validates the shape of the given pattern.

    The patterns must be dictionaries with exactly the keys in
    NUMBER_KEYS. Each value must be a dictionary with exactly the keys
    in CASE_NAMES. All case forms must be strings.

    Args:
        pattern: The object to validate.

    Returns:
        The validated pattern as type Pattern.

    Raises:
        ValueError: The pattern has an invalid type, unexpected keys,
            non-dictionary number values, incorrect case names, or
            non-string case forms.
    """

    if not isinstance(pattern, dict):
        raise ValueError(
            f"Expected each pattern to be {dict}, but received "
            f"{type(pattern)} in pattern {pattern}"
        )
    if tuple(pattern.keys()) != NUMBER_KEYS:
        raise ValueError(
            f"Expected each pattern to have the keys {sorted(NUMBER_KEYS)}, "
            f"but received {sorted(pattern.keys())} in pattern {pattern}"
        )

    for number in NUMBER_KEYS:
        cases = pattern[number]

        if not isinstance(cases, dict):
            raise ValueError(
                f"Expected {sorted(NUMBER_KEYS)} keys in each pattern to map "
                f"to {dict}, but {number} is mapped to {type(cases)} in "
                f"pattern {pattern}"
            )
        if tuple(cases.keys()) != CASE_NAMES:
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
    """Loads and validates all declension pattern found in the given
    JSON file.

    Each line in the file must contain a JSON object representing one
    declension pattern. This function reads each line as a compound
    dictionary, validates and places them in a list.

    Args:
        file_name: Name of the JSON file containing the declension
            patterns.

    Returns:
        A list of validated declension patterns. Each pattern maps
        grammatical numbers, such as "singular" and "plural", to
        dictionaries of case names and their corresponding forms.
    """

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
