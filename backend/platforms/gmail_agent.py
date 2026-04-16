# agents/platforms/gmail_agent.py
# STEP 138 — Gmail agent
#
# Four capabilities:
#   read_emails()     — open Gmail, scan inbox, return summary
#   send_email()      — send new email via SMTP (fast) or browser
#   reply_to_email()  — find email, click reply, type response, send
#   check_unread()    — quick unread count
#
# Browser mode: uses your logged-in Gmail session (no password needed)
# SMTP mode: sends directly via Python (needs GMAIL_APP_PASSWORD in .env)
#
# Usage:
#   from agents.platforms.gmail_agent import gmail
#   gmail.send("friend@gmail.com", "Hello", "How are you?")
#   gmail.read_emails()
#   gmail.reply_to_email("John", "Thanks for reaching out!")

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailAgent:

    def __init__(self):
        self.gmail_user     = os.getenv("GMAIL_USER", "")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")

    # -------------------------
    # SEND EMAIL
    # Fast SMTP if app password set, else browser fallback
    # -------------------------

    def send(self, to, subject, body, use_browser=False):
        """
        Send an email.

        Args:
            to: recipient email address
            subject: email subject
            body: email body text
            use_browser: force browser mode even if SMTP available
        """
        # load profile signature
        try:
            from brain.personal_profile import profile
            signature = profile.email_signature
            sender    = profile.primary_email
            full_body = f"{body}\n\n{signature}"
        except:
            sender    = self.gmail_user
            full_body = body

        if not use_browser and self.gmail_password and sender:
            return self._send_smtp(sender, to, subject, full_body)
        else:
            return self._send_browser(to, subject, full_body)

    def _send_smtp(self, sender, to, subject, body):
        """Send via SMTP — fast, no browser needed."""
        print(f"📧 Sending email to {to} via SMTP...")
        try:
            msg = MIMEMultipart()
            msg["From"]    = sender
            msg["To"]      = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, self.gmail_password)
                server.sendmail(sender, to, msg.as_string())

            print(f"✅ Email sent to {to}")
            return {"outcome": "success", "method": "smtp", "to": to}

        except Exception as e:
            print(f"SMTP error: {e} — falling back to browser")
            return self._send_browser(to, subject, body)

    def _send_browser(self, to, subject, body):
        """Send via Gmail browser — uses logged-in session."""
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"📧 Sending email to {to} via browser...")
        navigate_to_platform("gmail")

        goal = (
            f"on Gmail click compose, "
            f"type '{to}' in the To field, "
            f"type '{subject}' in the Subject field, "
            f"type '{body[:200]}' in the body, "
            f"click Send"
        )
        result = run_visual_goal(goal, max_steps=15)
        return result

    # -------------------------
    # READ EMAILS
    # Opens Gmail, reads inbox, returns summary
    # -------------------------

    def read_emails(self, max_emails=5):
        """
        Open Gmail and read unread emails.
        Returns list of email summaries.
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print("📬 Reading emails...")
        navigate_to_platform("gmail")

        goal = (
            f"on Gmail look at the inbox, "
            f"read the first {max_emails} unread emails, "
            f"for each email note the sender, subject and first line, "
            f"then mark as done"
        )
        result = run_visual_goal(goal, max_steps=20)

        # extract email summaries from steps
        summaries = self._extract_summaries(result.get("steps_taken", []))
        return {
            "outcome": result.get("outcome"),
            "emails": summaries,
            "steps": result.get("steps")
        }

    # -------------------------
    # REPLY TO EMAIL
    # -------------------------

    def reply_to_email(self, sender_name, reply_text):
        """
        Find an email from sender_name and reply to it.

        Args:
            sender_name: name or email of the sender to find
            reply_text: the reply message to send
        """
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        print(f"↩️  Replying to {sender_name}...")
        navigate_to_platform("gmail")

        goal = (
            f"on Gmail find the email from {sender_name}, "
            f"open it, click Reply, "
            f"type '{reply_text}', "
            f"click Send"
        )
        result = run_visual_goal(goal, max_steps=15)
        return result

    # -------------------------
    # CHECK UNREAD COUNT
    # -------------------------

    def check_unread(self):
        """Quick check of unread email count."""
        from execution.visual_agent import run_visual_goal
        from brain.tab_intelligence import navigate_to_platform

        navigate_to_platform("gmail")
        goal = "on Gmail check how many unread emails are in the inbox and report the number, then mark done"
        result = run_visual_goal(goal, max_steps=5)
        return result

    # -------------------------
    # WRITE EMAIL WITH AI
    # Generates email body using LLM
    # -------------------------

    def compose_with_ai(self, to, subject, instructions):
        """
        AI-compose an email then send it.

        Args:
            to: recipient
            subject: email subject
            instructions: what the email should say e.g. "follow up on my job application"
        """
        body = self._generate_email_body(subject, instructions)
        if body:
            print(f"AI composed email:\n{body[:200]}...")
            return self.send(to, subject, body)
        return {"outcome": "failed", "reason": "could not generate email body"}

    def _generate_email_body(self, subject, instructions):
        """Use LLM to write email body."""
        try:
            from openai import OpenAI
            key = os.getenv("GROQ_API_KEY")
            if not key:
                return instructions

            from brain.personal_profile import profile
            client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")

            prompt = f"""Write a professional email body.
Subject: {subject}
Instructions: {instructions}
Sender: {profile.name}
Sender email: {profile.email}

Write ONLY the email body. No subject line. No 'Dear...' unless natural.
End with the sender's name. Keep it concise and professional."""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Email compose error: {e}")
            return instructions

    # -------------------------
    # HELPER
    # -------------------------

    def _extract_summaries(self, steps_taken):
        """Extract email info from visual agent step descriptions."""
        summaries = []
        for step in steps_taken:
            screen = step.get("screen", "")
            if any(kw in screen.lower() for kw in ["inbox", "unread", "from:", "subject:"]):
                summaries.append(screen[:150])
        return summaries[:5]


# -------------------------
# GLOBAL INSTANCE
# -------------------------

gmail = GmailAgent()