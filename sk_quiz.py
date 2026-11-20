import json
from typing import Any, TypedDict, cast
from typing_extensions import ReadOnly
from enum import Enum, auto


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
type UserAnswers = dict[str, dict[str, str]]


class Action(Enum):
    BACK = auto()
    STOP = auto()
    FORWARD = auto()


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


def create_question_triples(pattern: Pattern) -> list[tuple[str, str, str]]:
    """Creates question triples from a pattern.

    Args:
        pattern: A compound dictionary containing the pattern used to
            create question triples.

    Returns:
        A list of (noun, number, case) tuples, one for each case under
        each number.
    """
    noun = pattern['singular']['nominative']
    return [
        (noun, number, case)
        for number in NUMBER_KEYS
        for case in pattern[number]
    ]


def ask_questions(
    questions: list[tuple[str, str, str]],
) -> tuple[Action, UserAnswers]:
    """Asks the user every question in the list, except for the
    nominative case, then saves their answers.

    Prints each question individually then prompts for a user input.
    The (first) nominative case is used to display the current noun.
    The inputs 'q', 'pn', 'pc' mean quit, return to the previous noun, 
    return to the previous case, respectively. Other inputs are saved 
    as answers.

    Args:
        questions: A list of (noun, number, case) tuples storing the
            questions.

    Returns:
        A tuple containing the action to take and the collected answers 
        (answers may be incomplete if the user quits or navigates back).
    """

    print(f"{questions[0][0].capitalize()}")
    user_answers: UserAnswers = {key: {} for key in NUMBER_KEYS}
    # Skip the nominative case
    curr_pos = 1
    while curr_pos < len(questions):
        _, number, case = questions[curr_pos]
        prompt = f"{number} {case}: "
        user_input = input(prompt).strip().lower()

        if user_input == 'q':
            return Action.STOP, user_answers
        elif user_input == 'pn':
            return Action.BACK, user_answers
        elif user_input == 'pc':
            curr_pos = max(curr_pos - 1, 1)
        else:
            user_answers[number][case] = user_input
            curr_pos += 1

    return Action.FORWARD, user_answers


def print_instructions() -> None:
    """Prints quiz navigation instructions."""

    print("Enter 'q' at any time to quit.")
    print("Enter 'pc' to return to previous case.")
    print("Enter 'pn' to return to prevous noun.\n")


def main():
    patterns = load_patterns()

    print_instructions()
    curr_pos = 0
    while curr_pos < len(patterns):
        curr_question = create_question_triples(patterns[curr_pos])

        action, answers = ask_questions(curr_question)

        if action is Action.FORWARD:
            curr_pos += 1
        elif action is Action.BACK:
            curr_pos = max(curr_pos - 1, 0)
        else:
            break


if __name__ == '__main__':
    main()
