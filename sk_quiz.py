import json


def load_patterns(file_name='slovak_declension_patterns.jsonl'):
    """Load and return all declension pattern found in the given file."""
    patterns = []
    with open(file_name, mode='r') as f:
        for pattern_str in f.readlines():
            patterns.append(json.loads(pattern_str))
    return patterns


def main():
    patterns = load_patterns()


if __name__ == '__main__':
    main()
