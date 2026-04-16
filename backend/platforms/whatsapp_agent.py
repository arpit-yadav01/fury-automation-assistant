# agents/platforms/whatsapp_agent.py
# STEP 139 — WhatsApp Web agent
#
# Controls web.whatsapp.com to:
#   send_message()   — find contact, type message, send
#   read_messages()  — read recent messages from a contact
#   reply_last()     — reply to the most recent message
#
# Requires WhatsApp Web to be open and logged in (QR scanned).
#
# Usage:
#   from agents.platforms.whatsapp_agent import whatsapp
#   whatsapp.send("John", "Hey, how are you?")
#   whatsapp.read("Mom")
#   whatsapp.reply_last("John", "Got it, thanks!")

import time


class WhatsAppAgent:

    # -------------------------
    # SEND MESSAGE
    # -------------------------

    def send(self, contact, message):
        """
        Send a WhatsApp message to a contact.

        Args:
            contact: contact name as it appears in WhatsApp
            message: text to send

        Returns:
            visual agent result dict
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"💬 WhatsApp → {contact}: {message[:50]}...")
        navigate_to_platform("whatsapp")
        time.sleep(2)

        goal = (
            f"on WhatsApp Web find the contact '{contact}' in the search bar, "
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
        Read recent messages from a contact.

        Args:
            contact: contact name
            count: how many recent messages to read
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"📖 Reading WhatsApp messages from {contact}...")
        navigate_to_platform("whatsapp")
        time.sleep(2)

        goal = (
            f"on WhatsApp Web find the chat with '{contact}', "
            f"open it, read the last {count} messages, "
            f"summarize what was said, then mark done"
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

        print(f"↩️  Replying to {contact} on WhatsApp...")
        navigate_to_platform("whatsapp")
        time.sleep(2)

        goal = (
            f"on WhatsApp Web open the chat with '{contact}', "
            f"click the message input at the bottom, "
            f"type '{reply_text}', "
            f"press Enter to send"
        )
        result = run_visual_goal(goal, max_steps=12)
        return result

    # -------------------------
    # AI REPLY
    # Reads last message and generates a smart reply
    # -------------------------

    def smart_reply(self, contact):
        """
        Read the last message from contact and generate + send a smart reply.
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"🤖 Smart reply to {contact}...")
        navigate_to_platform("whatsapp")
        time.sleep(2)

        goal = (
            f"on WhatsApp Web open the chat with '{contact}', "
            f"read the last message they sent, "
            f"type an appropriate friendly reply in the input box, "
            f"press Enter to send"
        )
        result = run_visual_goal(goal, max_steps=15)
        return result

    # -------------------------
    # CHECK UNREAD
    # -------------------------

    def check_unread(self):
        """Check which contacts have unread messages."""
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        navigate_to_platform("whatsapp")
        time.sleep(2)

        goal = (
            "on WhatsApp Web look at the chat list, "
            "identify which chats have unread messages (shown in green), "
            "list the contact names, then mark done"
        )
        result = run_visual_goal(goal, max_steps=8)
        return result

    # -------------------------
    # SEND TO MULTIPLE
    # -------------------------

    def broadcast(self, contacts, message):
        """
        Send the same message to multiple contacts.

        Args:
            contacts: list of contact names
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

whatsapp = WhatsAppAgent()