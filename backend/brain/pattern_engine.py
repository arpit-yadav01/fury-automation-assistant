from memory.experience_memory import load_experiences


def detect_patterns():

    data = load_experiences()

    patterns = {}

    for exp in data:

        cmd = exp["command"].lower()

        if cmd not in patterns:
            patterns[cmd] = 0

        patterns[cmd] += 1

    return patterns


def get_frequent_command(threshold=3):

    patterns = detect_patterns()

    frequent = []

    for cmd, count in patterns.items():

        if count >= threshold:
            frequent.append((cmd, count))

    return sorted(frequent, key=lambda x: -x[1])