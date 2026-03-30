def plan_ui_actions(task):

    if not isinstance(task, dict):
        return []

    intent = task.get("intent")

    actions = []

    # -----------------------
    # SEARCH CASE
    # -----------------------

    if intent == "web_search":

        query = task.get("query")

        actions = [
            {"action": "click_text", "text": "Search"},
            {"action": "type", "text": query},
            {"action": "enter"}
        ]

    return actions