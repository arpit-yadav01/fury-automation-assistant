# platforms/job_desc_parser.py
# STEP 141 — Job description parser
#
# Paste any job description → get tailored cover letter + email draft
# Uses your profile.yaml data — no form filling, no clicking Apply
#
# Usage:
#   from platforms.job_desc_parser import parse_and_generate
#   parse_and_generate(job_description_text)

import os
import re
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")


# -------------------------
# EXTRACT JOB DETAILS
# Pulls role, company, skills from raw job description text
# Zero tokens — pure regex + text parsing
# -------------------------

def extract_job_details(job_desc):
    """
    Extract structured info from raw job description text.
    No LLM needed — regex + keyword matching.

    Returns dict with: role, company, skills, experience, location
    """
    text = job_desc.strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    role    = _extract_role(text, lines)
    company = _extract_company(text, lines)
    skills  = _extract_skills(text)
    exp     = _extract_experience(text)
    loc     = _extract_location(text)

    return {
        "role":       role,
        "company":    company,
        "skills":     skills,
        "experience": exp,
        "location":   loc,
        "raw":        text[:500],
    }


def _extract_role(text, lines):
    """Find job title — usually in first 3 lines or after Role:/Position:/Title:"""
    patterns = [
        r"(?:role|position|title|job title|designation)\s*[:\-]\s*(.+)",
        r"(?:hiring|looking for|we need)\s+(?:a\s+)?(.+?)(?:\s+at|\s+to|\s+who|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text[:500], re.IGNORECASE)
        if m:
            return m.group(1).strip()[:60]

    # fallback — check first 3 lines for role keywords
    role_kws = ["developer", "engineer", "intern", "designer",
                "analyst", "manager", "architect", "lead"]
    for line in lines[:5]:
        if any(kw in line.lower() for kw in role_kws) and len(line) < 80:
            return line.strip()

    return lines[0][:60] if lines else "Software Developer"


def _extract_company(text, lines):
    """Find company name."""
    patterns = [
        r"(?:company|organization|firm|at)\s*[:\-]\s*(.+)",
        r"(?:join|joining)\s+([A-Z][a-zA-Z\s]+?)(?:\s+as|\s+team|\.|,)",
        r"^([A-Z][a-zA-Z\s&]+(?:Inc|Ltd|Pvt|Corp|Solutions|Technologies|Systems)?)",
    ]
    for pat in patterns:
        m = re.search(pat, text[:400], re.IGNORECASE | re.MULTILINE)
        if m:
            company = m.group(1).strip()
            if 2 < len(company) < 50:
                return company

    # check first few lines for capitalized company name
    for line in lines[:4]:
        if line[0].isupper() and len(line) < 40 and not any(
            kw in line.lower() for kw in ["developer", "required", "job", "we are"]
        ):
            return line

    return "the company"


def _extract_skills(text):
    """Find required technical skills."""
    known_skills = [
        "react", "node.js", "nodejs", "javascript", "typescript",
        "python", "java", "html", "css", "mongodb", "postgresql",
        "mysql", "sql", "express", "next.js", "nextjs", "vue",
        "angular", "django", "flask", "fastapi", "rest api",
        "graphql", "docker", "kubernetes", "aws", "git", "github",
        "mern", "mean", "redux", "tailwind", "bootstrap",
        "react native", "flutter", "firebase", "linux",
    ]
    text_lower = text.lower()
    found = [s for s in known_skills if s in text_lower]
    return found[:8]  # top 8 matches


def _extract_experience(text):
    """Find experience requirement."""
    patterns = [
        r"(\d+[\+\-]?\s*(?:to\s*\d+)?\s*years?\s*(?:of\s+)?experience)",
        r"experience\s*[:\-]\s*(\d+[\+]?\s*years?)",
        r"(\d+[\+]?\s*years?\s*(?:of\s+)?(?:relevant\s+)?experience)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return "0-2 years"


def _extract_location(text):
    """Find job location."""
    patterns = [
        r"(?:location|office|based in|city)\s*[:\-]\s*(.+)",
        r"(?:remote|hybrid|onsite|work from home)",
    ]
    for pat in patterns:
        m = re.search(pat, text[:500], re.IGNORECASE)
        if m:
            loc = m.group(0).strip() if not m.lastindex else m.group(1).strip()
            return loc[:40]
    return "India"


# -------------------------
# GENERATE COVER LETTER
# Uses profile + job details — ~80 tokens for custom paragraph
# -------------------------

def generate_cover_letter(job_details):
    """Generate tailored cover letter from job details + profile."""
    from brain.personal_profile import profile

    role    = job_details.get("role", "Software Developer")
    company = job_details.get("company", "the company")
    req_skills = job_details.get("skills", [])

    # find matching skills between job requirements and candidate
    my_skills = [s.lower() for s in profile.all_skills_flat]
    matching  = [s for s in req_skills if s.lower() in my_skills]
    if not matching:
        matching = profile.all_skills_flat[:3]

    # generate custom paragraph — ~80 tokens
    custom = _custom_paragraph(role, company, matching,
                                job_details.get("raw", ""), profile)

    # fill template
    template = profile._cover.get("template", _default_template())
    letter = (template
              .replace("{role}", role)
              .replace("{company}", company)
              .replace("{custom_paragraph}", custom))

    return letter


def _custom_paragraph(role, company, skills, job_desc, profile):
    """Generate 2-sentence custom paragraph — ~80 tokens."""
    if not client:
        return (
            f"My experience with {', '.join(skills[:3])} makes me a strong fit "
            f"for this {role} role. I am excited about contributing to "
            f"{company}'s team."
        )
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content":
                f"Write exactly 2 sentences for a cover letter body paragraph.\n"
                f"Role: {role} at {company}\n"
                f"Candidate skills: {', '.join(skills[:4])}\n"
                f"Job needs: {job_desc[:150]}\n"
                f"Be specific and professional. Only 2 sentences."
            }],
            temperature=0.2,
            max_tokens=80
        )
        return resp.choices[0].message.content.strip()
    except:
        return (
            f"My hands-on experience with {', '.join(skills[:3])} "
            f"aligns directly with the requirements for this {role} position."
        )


def _default_template():
    return (
        "Dear Hiring Manager,\n\n"
        "I am writing to express my interest in the {role} position at {company}.\n\n"
        "{custom_paragraph}\n\n"
        "I would welcome the opportunity to discuss how my background aligns "
        "with your requirements.\n\n"
        "Best regards,\nArpit Yadav\n"
        "arpityadav170402@gmail.com | +91-9027706195"
    )


# -------------------------
# GENERATE EMAIL DRAFT
# Zero tokens — built from template
# -------------------------

def generate_email(job_details, to_email=None):
    """Generate application email — zero tokens."""
    from brain.personal_profile import profile

    role    = job_details.get("role", "Software Developer")
    company = job_details.get("company", "the company")
    skills  = job_details.get("skills", [])
    my_exp  = profile._exp[0]["role"] if profile._exp else "Software Developer"

    subject = f"Application for {role} Position — {profile.name}"
    body    = (
        f"Dear Hiring Manager,\n\n"
        f"I am interested in the {role} position at {company}. "
        f"I currently work as a {my_exp} with hands-on experience in "
        f"{', '.join(skills[:3] or profile.all_skills_flat[:3])}.\n\n"
        f"I believe my background aligns well with your requirements and "
        f"I would love the opportunity to contribute to your team.\n\n"
        f"Please find my resume attached. I look forward to hearing from you.\n\n"
        f"{profile.email_signature}"
    )

    return {
        "to":      to_email or "(paste HR email here)",
        "subject": subject,
        "body":    body,
    }


# -------------------------
# MAIN ENTRY POINT
# Paste job description → get everything
# -------------------------

def parse_and_generate(job_desc_text, to_email=None):
    """
    Main function — paste job description, get cover letter + email.

    Args:
        job_desc_text: raw job description (paste from Naukri/LinkedIn/etc)
        to_email: HR email address if known

    Returns:
        dict with job_details, cover_letter, email
    """
    if not job_desc_text or len(job_desc_text.strip()) < 20:
        return {"error": "Job description too short — paste the full text"}

    print("\n📋 Parsing job description...")

    # extract details — zero tokens
    details = extract_job_details(job_desc_text)
    print(f"   Role    : {details['role']}")
    print(f"   Company : {details['company']}")
    print(f"   Skills  : {', '.join(details['skills']) or 'not detected'}")
    print(f"   Exp req : {details['experience']}")

    # generate cover letter — ~80 tokens
    print("\n✍️  Generating cover letter...")
    letter = generate_cover_letter(details)

    # generate email — zero tokens
    print("📧 Generating email draft...")
    email  = generate_email(details, to_email)

    # print results
    _print_results(details, letter, email)

    return {
        "job_details":   details,
        "cover_letter":  letter,
        "email":         email,
    }


def _print_results(details, letter, email):
    print(f"\n{'='*60}")
    print(f"JOB: {details['role']} at {details['company']}")
    print(f"{'='*60}")

    print("\n📄 COVER LETTER")
    print("─" * 60)
    print(letter)

    print(f"\n{'='*60}")
    print("📧 EMAIL DRAFT — copy and send manually from Gmail")
    print("─" * 60)
    print(f"TO     : {email['to']}")
    print(f"SUBJECT: {email['subject']}")
    print(f"BODY   :")
    print(email["body"])
    print(f"{'='*60}")
    print("⚠️  Send manually — Fury does NOT send it automatically\n")