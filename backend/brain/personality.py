def respond(event):

    if event == "start":
        return "🔥 Fury ready."

    if event == "executing":
        return "⚡ Executing..."

    if event == "done":
        return "✅ Done."

    if event == "error":
        return "⚠️ Something went wrong."

    if event == "learn":
        return "🧠 Learning from experience..."

    if event == "thinking":
        return "🧠 Thinking..."

    if event == "memory":
        return "💾 Using memory..."

    return ""