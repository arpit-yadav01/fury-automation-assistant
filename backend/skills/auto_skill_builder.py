from memory.experience_memory import load_experiences

AUTO_SKILLS = {}
THRESHOLD = 3


def normalize(command):
    return command.lower().strip()


def build_auto_skills():

    AUTO_SKILLS.clear()

    data = load_experiences()

    counter = {}

    for exp in data:

        cmd = normalize(exp.get("command", ""))

        if cmd not in counter:
            counter[cmd] = []

        counter[cmd].append(exp)

    for cmd, logs in counter.items():

        if len(logs) >= THRESHOLD:

            skill_name = generate_skill_name(cmd)

            AUTO_SKILLS[skill_name] = {
                "plan": logs[-1].get("plan"),
                "command": cmd
            }

    return AUTO_SKILLS


# ✅ FIXED — STRICT MATCH
def find_best_skill(user_command):

    user_command = normalize(user_command)

    skills = build_auto_skills()

    for name, data in skills.items():

        cmd = data.get("command")
        plan = data.get("plan")

        if not cmd or not plan:
            continue

        # ✅ ONLY EXACT MATCH
        if user_command == cmd:
            return name, plan

    return None, None


def generate_skill_name(command):

    if "youtube" in command and "lofi" in command:
        return "play_lofi"

    if "youtube" in command and "music" in command:
        return "play_music"

    if "google" in command:
        return "search_google"

    return command.replace(" ", "_")[:30]