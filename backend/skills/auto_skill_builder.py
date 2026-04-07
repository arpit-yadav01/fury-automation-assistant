from memory.experience_memory import load_experiences

AUTO_SKILLS = {}
THRESHOLD = 3


def normalize(command):
    return command.lower().strip()


# =========================
# BUILD SKILLS
# =========================

def build_auto_skills():

    AUTO_SKILLS.clear()  # 🔥 important

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


# =========================
# 🔥 STEP 105 — SMART MATCH
# =========================

def find_best_skill(user_command):

    user_command = normalize(user_command)

    skills = build_auto_skills()

    for name, data in skills.items():

        cmd = data.get("command", "")
        plan = data.get("plan")

        if not cmd or not plan:
            continue

        # exact contains
        if cmd in user_command:
            return name, plan

        # partial match
        words = cmd.split()

        match_count = sum(1 for w in words if w in user_command)

        if match_count >= max(1, len(words) // 2):
            return name, plan

    return None, None


# =========================
# NAME GENERATOR
# =========================

def generate_skill_name(command):

    if "youtube" in command and "lofi" in command:
        return "play_lofi"

    if "youtube" in command and "music" in command:
        return "play_music"

    if "google" in command:
        return "search_google"

    return command.replace(" ", "_")[:30]


# =========================
# DEBUG (optional)
# =========================

if __name__ == "__main__":
    print(build_auto_skills())