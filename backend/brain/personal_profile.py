# brain/personal_profile.py
# STEP 135 — Personal profile
#
# Loads profile.yaml and provides Arpit's personal data
# to every agent that needs it — job applications, emails,
# form filling, cover letters, etc.
#
# Usage:
#   from brain.personal_profile import profile
#   name  = profile.name
#   email = profile.email
#   skills = profile.skills
#   cover = profile.generate_cover_letter("React Developer", "Google")

import os
import yaml
from types import SimpleNamespace

_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(_DIR, "profile.yaml")


def _load():
    if not os.path.exists(PROFILE_PATH):
        print(f"Profile not found at {PROFILE_PATH}")
        return {}
    try:
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Profile load error: {e}")
        return {}


class PersonalProfile:
    """
    Provides structured access to profile.yaml.
    All agents read from this single source of truth.
    """

    def __init__(self):
        self._data = _load()
        self._identity  = self._data.get("identity", {})
        self._resume    = self._data.get("resume", {})
        self._skills    = self._data.get("skills", {})
        self._exp       = self._data.get("experience", [])
        self._edu       = self._data.get("education", {})
        self._prefs     = self._data.get("job_preferences", {})
        self._platforms = self._data.get("platforms", {})
        self._email     = self._data.get("email", {})
        self._cover     = self._data.get("cover_letter", {})

    def reload(self):
        """Reload profile from disk (call after editing profile.yaml)."""
        self.__init__()

    # -------------------------
    # IDENTITY
    # -------------------------

    @property
    def name(self):
        return self._identity.get("name", "")

    @property
    def email(self):
        return self._identity.get("email", "")

    @property
    def phone(self):
        return self._identity.get("phone", "")

    @property
    def location(self):
        return self._identity.get("location", "")

    @property
    def github(self):
        return self._identity.get("github", "")

    @property
    def linkedin(self):
        return self._identity.get("linkedin", "")

    # -------------------------
    # RESUME
    # -------------------------

    @property
    def resume_path(self):
        return self._resume.get("path", "")

    @property
    def resume_summary(self):
        return self._resume.get("summary", "")

    # -------------------------
    # SKILLS
    # -------------------------

    @property
    def skills(self):
        return self._skills

    @property
    def all_skills_flat(self):
        """All skills as a flat list."""
        flat = []
        for v in self._skills.values():
            if isinstance(v, list):
                flat.extend(v)
        return flat

    @property
    def primary_stack(self):
        return self._prefs.get("stack", "MERN")

    # -------------------------
    # JOB PREFERENCES
    # -------------------------

    @property
    def target_roles(self):
        return self._prefs.get("roles", [])

    @property
    def job_types(self):
        return self._prefs.get("type", ["full-time"])

    def is_relevant_job(self, job_title, required_skills=None):
        """
        Check if a job matches Arpit's preferences.
        Used by job application agents to filter roles.
        """
        title_lower = job_title.lower()

        # check role match
        role_keywords = [
            "mern", "react", "node", "javascript", "fullstack",
            "full stack", "full-stack", "frontend", "backend",
            "software developer", "software engineer", "web developer"
        ]
        role_match = any(kw in title_lower for kw in role_keywords)

        # check skill match if provided
        skill_match = True
        if required_skills:
            my_skills = [s.lower() for s in self.all_skills_flat]
            matched = sum(1 for s in required_skills if s.lower() in my_skills)
            skill_match = matched >= len(required_skills) * 0.5

        return role_match and skill_match

    # -------------------------
    # PLATFORMS
    # -------------------------

    def get_platform(self, name):
        """Get platform config by name."""
        return self._platforms.get(name.lower(), {})

    def get_platform_url(self, name):
        """Get URL for a platform."""
        p = self.get_platform(name)
        return p.get("url", "")

    def get_all_platform_urls(self):
        """Get all platform URLs as a dict."""
        return {
            name: data.get("url", "")
            for name, data in self._platforms.items()
        }

    # -------------------------
    # EMAIL
    # -------------------------

    @property
    def primary_email(self):
        return self._email.get("primary", self.email)

    @property
    def email_provider(self):
        return self._email.get("provider", "gmail")

    @property
    def email_signature(self):
        return self._email.get("signature", f"Best regards,\n{self.name}")

    # -------------------------
    # COVER LETTER
    # -------------------------

    def generate_cover_letter(self, role, company, job_desc=None):
        """
        Generate a tailored cover letter for a specific role.
        Uses LLM to customize the middle paragraph.
        """
        template = self._cover.get("template", "")

        # generate custom paragraph with LLM if available
        custom = self._generate_custom_paragraph(role, company, job_desc)

        letter = template.replace("{role}", role)
        letter = letter.replace("{company}", company)
        letter = letter.replace("{custom_paragraph}", custom)

        return letter

    def _generate_custom_paragraph(self, role, company, job_desc):
        """Use LLM to write a tailored paragraph."""
        try:
            import os
            from openai import OpenAI
            key = os.getenv("GROQ_API_KEY")
            if not key:
                return self._default_paragraph(role)

            client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")

            prompt = f"""Write ONE paragraph (3-4 sentences) for a cover letter.
Candidate: {self.name}
Role: {role} at {company}
Candidate skills: {', '.join(self.all_skills_flat[:10])}
Candidate summary: {self.resume_summary}
Job description: {(job_desc or '')[:500]}

Write only the paragraph. No greeting. No sign-off. Make it specific and genuine."""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return self._default_paragraph(role)

    def _default_paragraph(self, role):
        return (
            f"My experience with React.js, Node.js, and the MERN stack "
            f"makes me well-suited for this {role} role. I have built "
            f"full-stack applications, integrated RESTful APIs, and "
            f"delivered responsive interfaces across multiple projects."
        )

    # -------------------------
    # FORM FILL CONTEXT
    # Returns dict used by visual agent to fill application forms
    # -------------------------

    def get_form_context(self, platform=None, role=None, company=None):
        """
        Returns a dict with all info needed to fill a job application form.
        Visual agent passes this as context to each step.
        """
        return {
            "name": self.name,
            "email": self.primary_email,
            "phone": self.phone,
            "location": self.location,
            "github": self.github,
            "linkedin": self.linkedin,
            "resume_path": self.resume_path,
            "role": role or self.target_roles[0],
            "company": company or "",
            "skills_summary": ", ".join(self.all_skills_flat[:8]),
            "experience_years": "1+",
            "current_role": self._exp[0]["role"] if self._exp else "",
            "current_company": self._exp[0]["company"] if self._exp else "",
            "education": f"{self._edu.get('degree')} — {self._edu.get('university')}",
            "cover_letter": self.generate_cover_letter(
                role or self.target_roles[0],
                company or "the company"
            ) if role or company else "",
        }

    # -------------------------
    # DEBUG
    # -------------------------

    def show(self):
        print("\n--- Fury Profile ---")
        print(f"Name    : {self.name}")
        print(f"Email   : {self.email}")
        print(f"Phone   : {self.phone}")
        print(f"Stack   : {self.primary_stack}")
        print(f"Roles   : {', '.join(self.target_roles[:3])}")
        print(f"Skills  : {', '.join(self.all_skills_flat[:6])}")
        print(f"Resume  : {self.resume_path or 'not set'}")
        print(f"Platforms: {', '.join(self._platforms.keys())}")
        print("--------------------\n")


# -------------------------
# GLOBAL INSTANCE
# -------------------------

profile = PersonalProfile()