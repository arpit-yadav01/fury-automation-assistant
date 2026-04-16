# agents/platforms/telegram_agent.py
# STEP 140 — Telegram Web agent
#
# Controls web.telegram.org to:
#   send_message()   — find contact/group, type message, send
#   read_messages()  — read recent messages from a contact
#   reply_last()     — reply to most recent message
#   check_unread()   — check which chats have unread messages
#
# Requires Telegram Web to be open and logged in.
#
# Usage:
#   from agents.platforms.telegram_agent import telegram
#   telegram.send("John", "Hey, how are you?")
#   telegram.read("Dev Group")
#   telegram.reply_last("John", "Got it!")

import time


class TelegramAgent:

    # -------------------------
    # SEND MESSAGE
    # -------------------------

    def send(self, contact, message):
        """
        Send a Telegram message to a contact or group.

        Args:
            contact: contact name or group name as shown in Telegram
            message: text message to send

        Returns:
            visual agent result dict
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"✈️  Telegram → {contact}: {message[:50]}...")
        navigate_to_platform("telegram")
        time.sleep(2)

        goal = (
            f"on Telegram Web find the chat with '{contact}' "
            f"using the search bar at the top left, "
            f"click on the chat, "
            f"click the message input box at the bottom, "
            f"type '{message}', "
            f"press Enter to send"
        )
        result = run_visual_goal(goal, max_steps=15)
        return result

    # -------------------------
    # READ MESSAGES
    # -------------------------

    def read(self, contact, count=5):
        """
        Read recent messages from a contact or group.

        Args:
            contact: contact or group name
            count: how many recent messages to read
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"📖 Reading Telegram messages from {contact}...")
        navigate_to_platform("telegram")
        time.sleep(2)

        goal = (
            f"on Telegram Web search for '{contact}' in the search bar, "
            f"open the chat, "
            f"read the last {count} messages, "
            f"summarize what was discussed, "
            f"then mark done"
        )
        result = run_visual_goal(goal, max_steps=12)
        return result

    # -------------------------
    # REPLY TO LAST MESSAGE
    # -------------------------

    def reply_last(self, contact, reply_text):
        """Reply to the most recent message from a contact."""
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"↩️  Replying to {contact} on Telegram...")
        navigate_to_platform("telegram")
        time.sleep(2)

        goal = (
            f"on Telegram Web search for and open the chat with '{contact}', "
            f"click the message input box at the bottom, "
            f"type '{reply_text}', "
            f"press Enter to send"
        )
        result = run_visual_goal(goal, max_steps=12)
        return result

    # -------------------------
    # CHECK UNREAD
    # -------------------------

    def check_unread(self):
        """Check which chats have unread messages."""
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print("🔔 Checking Telegram unread messages...")
        navigate_to_platform("telegram")
        time.sleep(2)

        goal = (
            "on Telegram Web look at the chat list on the left, "
            "identify all chats that have unread message counts shown, "
            "list their names and unread counts, "
            "then mark done"
        )
        result = run_visual_goal(goal, max_steps=8)
        return result

    # -------------------------
    # SEND TO GROUP
    # -------------------------

    def send_to_group(self, group_name, message):
        """Send a message to a Telegram group."""
        return self.send(group_name, message)

    # -------------------------
    # SMART REPLY
    # Reads last message and generates intelligent reply
    # -------------------------

    def smart_reply(self, contact):
        """
        Read the last message from contact and
        generate + send a contextual reply.
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"🤖 Smart reply to {contact} on Telegram...")
        navigate_to_platform("telegram")
        time.sleep(2)

        goal = (
            f"on Telegram Web open the chat with '{contact}', "
            f"read the last message they sent, "
            f"type an appropriate friendly reply in the message box, "
            f"press Enter to send"
        )
        result = run_visual_goal(goal, max_steps=15)
        return result

    # -------------------------
    # BROADCAST
    # Send same message to multiple contacts
    # -------------------------

    def broadcast(self, contacts, message):
        """
        Send the same message to multiple Telegram contacts.

        Args:
            contacts: list of contact or group names
            message: message to send to all
        """
        results = []
        for contact in contacts:
            print(f"Sending to {contact}...")
            result = self.send(contact, message)
            results.append({
                "contact": contact,
                "outcome": result.get("outcome")
            })
            time.sleep(1)

        success = sum(1 for r in results if r["outcome"] == "success")
        print(f"\n📊 Sent to {success}/{len(contacts)} contacts")
        return results


# -------------------------
# GLOBAL INSTANCE
# -------------------------

telegram = TelegramAgent()