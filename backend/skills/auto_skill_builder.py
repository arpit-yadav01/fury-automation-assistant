from memory.experience_memory import load_memory

AUTO_SKILLS = {}
THRESHOLD = 3


def normalize(command):
    return command.lower().strip()


def build_auto_skills():

    AUTO_SKILLS.clear()  # 🔥 prevent duplication

    data = load_experiences()

    counter = {}

    for exp in data:

        cmd = normalize(exp["command"])

        if cmd not in counter:
            counter[cmd] = []

        counter[cmd].append(exp)

    for cmd, logs in counter.items():

        if len(logs) >= THRESHOLD:

            skill_name = generate_skill_name(cmd)

            AUTO_SKILLS[skill_name] = {
                "plan": logs[-1]["plan"],
                "command": cmd
            }

    return AUTO_SKILLS


def generate_skill_name(command):

    if "youtube" in command and "lofi" in command:
        return "play_lofi"

    if "google" in command:
        return "search_google"

    return command.replace(" ", "_")[:30]