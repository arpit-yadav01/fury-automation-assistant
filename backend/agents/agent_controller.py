# from agents.agent_registry import registry


# class AgentController:

#     def __init__(self):
#         pass

#     # -------------------------

#     def execute(self, plan):

#         if not plan:
#             return

#         # =========================
#         # LIST HANDLING
#         # =========================

#         if isinstance(plan, list):

#             for step in plan:
#                 self.execute(step)

#             return

#         current = plan

#         # =========================
#         # MAIN LOOP
#         # =========================

#         for _ in range(10):

#             # -------------------------
#             # WORKFLOW DIRECT EXECUTION
#             # -------------------------

#             if isinstance(current, dict) and "workflow" in current:
#                 self._execute_workflow(current["workflow"])
#                 return

#             # -------------------------
#             # DICT TASK
#             # -------------------------

#             if isinstance(current, dict):

#                 agent = registry.find_agent(current)

#                 if not agent:
#                     print("No agent for task:", current)
#                     return

#                 try:

#                     print("Agent:", agent.name)

#                     result = agent.handle(current)

#                     # =========================
#                     # 🔥 CRITICAL FIX — PLANNER HANDOFF
#                     # =========================

#                     from execution.task_planner import create_plan

#                     # parse_command → planner
#                     if isinstance(result, dict) and result.get("intent") == "parse_command":
#                         result = create_plan(result.get("text"))

#                     # string fallback → planner
#                     if isinstance(result, str):
#                         result = create_plan(result)

#                     # continue chain
#                     if isinstance(result, dict) or isinstance(result, list):

#     # 🔥 PREVENT SAME LOOP
#                         if result == current:
#                             return  

#                         current = result
#                         continue

#                     return

#                 except Exception as e:

#                     print("Agent error:", e)

#                     from agents.error_agent import ErrorRecoveryAgent

#                     err = ErrorRecoveryAgent()
#                     ok = err.handle_error(current, e)

#                     if not ok:
#                         print("Task failed:", current)

#                     return

#             # -------------------------
#             # STRING INPUT
#             # -------------------------

#             if isinstance(current, str):

#                 agent = registry.find_agent(current)

#                 if not agent:
#                     print("No agent for input:", current)
#                     return

#                 try:

#                     print("Agent:", agent.name)

#                     result = agent.handle(current)

#                     # 🔥 SAME FIX FOR STRING FLOW
#                     from execution.task_planner import create_plan

#                     if isinstance(result, dict) and result.get("intent") == "parse_command":
#                         result = create_plan(result.get("text"))

#                     if isinstance(result, str):
#                         result = create_plan(result)

#                     if isinstance(result, dict) or isinstance(result, list):
#                         current = result
#                         continue

#                     return

#                 except Exception as e:

#                     print("Agent error:", e)
#                     return

#         print("Controller loop limit reached")

#     # -------------------------

#     def _execute_workflow(self, steps):

#         for step in steps:

#             agent = registry.find_agent(step)

#             if not agent:
#                 print("No agent for step:", step)
#                 continue

#             try:

#                 print("Agent:", agent.name)

#                 result = agent.handle(step)

#                 if isinstance(result, dict) or isinstance(result, list):
#                     self.execute(result)

#             except Exception as e:

#                 print("Agent error:", e)


# # -------------------------
# # GLOBAL
# # -------------------------

# controller = AgentController()

# agents/agent_controller.py
# STEP 116 — confidence check added before agent.handle()

from agents.agent_registry import registry


class AgentController:

    def __init__(self):
        pass

    # -------------------------

    def execute(self, plan):

        if not plan:
            return

        # =========================
        # LIST HANDLING
        # =========================

        if isinstance(plan, list):
            for step in plan:
                self.execute(step)
            return

        current = plan

        # =========================
        # MAIN LOOP
        # =========================

        for _ in range(10):

            # -------------------------
            # WORKFLOW DIRECT EXECUTION
            # -------------------------

            if isinstance(current, dict) and "workflow" in current:
                self._execute_workflow(current["workflow"])
                return

            # -------------------------
            # DICT TASK
            # -------------------------

            if isinstance(current, dict):

                agent = registry.find_agent(current)

                if not agent:
                    print("No agent for task:", current)
                    return

                try:

                    # STEP 116 — confidence check
                    conf = agent.confidence(current)
                    decision = conf.get("decision", "proceed")

                    if decision == "abort":
                        print(f"Fury: not confident enough to run this.")
                        print(f"Reason: {conf.get('reason')}")
                        return

                    if decision == "ask":
                        if conf.get("risky"):
                            print(f"\nFury: ⚠️  This action is risky — {conf.get('reason')}")
                        else:
                            print(f"\nFury: Just checking — {conf.get('reason')}")
                        print("Proceed? (yes/no)")
                        answer = input(">>> ").strip().lower()
                        if answer not in ("yes", "y"):
                            print("Fury: Cancelled.")
                            return

                    print("Agent:", agent.name)
                    result = agent.handle(current)

                    # =========================
                    # PLANNER HANDOFF
                    # =========================

                    from execution.task_planner import create_plan

                    if isinstance(result, dict) and result.get("intent") == "parse_command":
                        result = create_plan(result.get("text"))

                    if isinstance(result, str):
                        result = create_plan(result)

                    if isinstance(result, dict) or isinstance(result, list):
                        if result == current:
                            return
                        current = result
                        continue

                    return

                except Exception as e:

                    print("Agent error:", e)

                    from agents.error_agent import ErrorRecoveryAgent
                    err = ErrorRecoveryAgent()
                    ok = err.handle_error(current, e)

                    if not ok:
                        print("Task failed:", current)

                    return

            # -------------------------
            # STRING INPUT
            # -------------------------

            if isinstance(current, str):

                agent = registry.find_agent(current)

                if not agent:
                    print("No agent for input:", current)
                    return

                try:

                    # STEP 116 — confidence check for string tasks too
                    pseudo_task = {"intent": "unknown", "raw": current}
                    conf = agent.confidence(pseudo_task)

                    if conf.get("decision") == "abort":
                        print(f"Fury: cannot handle '{current}' confidently.")
                        return

                    print("Agent:", agent.name)
                    result = agent.handle(current)

                    from execution.task_planner import create_plan

                    if isinstance(result, dict) and result.get("intent") == "parse_command":
                        result = create_plan(result.get("text"))

                    if isinstance(result, str):
                        result = create_plan(result)

                    if isinstance(result, dict) or isinstance(result, list):
                        current = result
                        continue

                    return

                except Exception as e:
                    print("Agent error:", e)
                    return

        print("Controller loop limit reached")

    # -------------------------

    def _execute_workflow(self, steps):

        for step in steps:

            agent = registry.find_agent(step)

            if not agent:
                print("No agent for step:", step)
                continue

            try:

                print("Agent:", agent.name)
                result = agent.handle(step)

                if isinstance(result, dict) or isinstance(result, list):
                    self.execute(result)

            except Exception as e:
                print("Agent error:", e)


# -------------------------
# GLOBAL
# -------------------------

controller = AgentController()
