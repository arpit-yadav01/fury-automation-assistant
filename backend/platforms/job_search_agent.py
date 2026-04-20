# platforms/job_search_agent.py
# SAFE job agent — read only
# Searches jobs, reads listings, generates cover letters
# NEVER fills forms, NEVER clicks Apply, NEVER submits anything
#
# Usage:
#   search jobs react developer naukri
#   read job https://www.naukri.com/job-listings/...
#   write cover letter React Developer TechCorp
#   draft email hr@company.com React Developer

import os
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

# -------------------------
# SEARCH URLS — read only, just open browser
# -------------------------

SEARCH_URLS = {
    "naukri":      "https://www.naukri.com/{query}-jobs",
    "indeed":      "https://www.indeed.com/jobs?q={query}&l=India",
    "internshala": "https://internshala.com/internships/{query}-internship",
    "linkedin":    "https://www.linkedin.com/jobs/search/?keywords={query}&location=India",
    "monster":     "https://www.foundit.in/srp/results?query={query}&location=India",
    "unstop":      "https://unstop.com/jobs?searchTerm={query}",
    "wellfound":   "https://wellfound.com/jobs?q={query}",
}


def search_jobs(query, platform="naukri"):
    """
    Open job search results in browser.
    Read only — just shows you the listings.
    YOU decide which ones to apply to.
    """
    from browser.browser_agent import open_website

    encoded = query.replace(" ", "-").lower()
    url = SEARCH_URLS.get(platform.lower(), "").replace("{query}", encoded)

    if not url:
        url = f"https://www.{platform}.com/jobs?q={query.replace(' ', '+')}"

    print(f"\n🔍 Searching {platform} for: {query}")
    print(f"   Opening: {url}")
    print(f"   ℹ️  Browse the results yourself — Fury will not click Apply")
    open_website(url)
    return {"platform": platform, "query": query, "url": url}


def read_job_details(url):
    """
    Open a job listing URL in browser so you can read it.
    Returns the URL for reference.
    """
    from browser.browser_agent import open_website
    print(f"\n📄 Opening job listing: {url}")
    open_website(url)
    return {"url": url}


def generate_cover_letter(role, company, job_description=None):
    """
    Generate a tailored cover letter using your profile.
    Prints it to terminal — YOU copy and send it yourself.
    """
    from brain.personal_profile import profile

    print(f"\n✍️  Generating cover letter for {role} at {company}...")

    letter = profile.generate_cover_letter(role, company, job_description)

    print("\n" + "="*60)
    print("COVER LETTER — copy this and send manually")
    print("="*60)
    print(letter)
    print("="*60 + "\n")

    return letter


def draft_email(to_email, role, company, job_description=None):
    """
    Draft a job application email.
    Prints subject + body — YOU send it yourself from Gmail.
    Does NOT send automatically.
    """
    from brain.personal_profile import profile

    subject = f"Application for {role} Position — {profile.name}"

    print(f"\n📧 Drafting email for {role} at {company}...")

    body = _generate_email_body(role, company, job_description, profile)

    print("\n" + "="*60)
    print("EMAIL DRAFT — copy this and send from your Gmail")
    print("="*60)
    print(f"TO      : {to_email}")
    print(f"SUBJECT : {subject}")
    print(f"BODY    :")
    print(body)
    print("="*60)
    print("⚠️  Send this yourself from Gmail — Fury will NOT send it")
    print("="*60 + "\n")

    return {"to": to_email, "subject": subject, "body": body}


def _generate_email_body(role, company, job_desc, profile):
    """Generate email body using LLM."""
    if not client:
        return profile.generate_cover_letter(role, company, job_desc)

    try:
        prompt = f"""Write a professional job application email body.

Candidate: {profile.name}
Role: {role}
Company: {company}
Skills: {', '.join(profile.all_skills_flat[:8])}
Experience: {profile.experience[0]['role'] if profile._exp else 'Software Developer'}
Job description: {(job_desc or 'Not provided')[:400]}

Write ONLY the email body (2-3 short paragraphs).
Start with Dear Hiring Manager.
End with the candidate's name and contact.
Keep it professional and specific to the role."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Email generation error: {e}")
        return profile.generate_cover_letter(role, company, job_desc)