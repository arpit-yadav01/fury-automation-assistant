# commands/job_commands.py
# Handles: job search, cover letter, email draft, job description parser
# Steps 137, 141


def handle(command, cmd):

    # ── STEP 137 — JOB SEARCH ────────────────
    if cmd.startswith("search jobs "):
        rest  = command[12:].strip()
        known = ["naukri", "indeed", "internshala", "linkedin",
                 "monster", "unstop", "wellfound"]
        parts = rest.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].lower() in known:
            query, platform = parts[0].strip(), parts[1].lower()
        else:
            query, platform = rest, "naukri"
        from platforms.job_search_agent import search_jobs
        search_jobs(query, platform)
        return True

    if cmd.startswith("read job "):
        from platforms.job_search_agent import read_job_details
        read_job_details(command[9:].strip())
        return True

    # ── STEP 141 — JOB DESC PARSER ───────────
    # Auto-detect pasted job description (long text with job keywords)
    if len(command) > 200 and any(kw in cmd for kw in [
        "experience", "required", "skills", "developer", "engineer",
        "responsibilities", "qualification", "salary", "apply",
        "role", "position", "hiring", "vacancy"
    ]):
        from platforms.job_desc_parser import parse_and_generate
        print("\n📋 Job description detected — generating cover letter + email...")
        parse_and_generate(command)
        return True

    if cmd.startswith("parse job "):
        from platforms.job_desc_parser import parse_and_generate
        parse_and_generate(command[10:].strip())
        return True

    if cmd.startswith("cover letter for "):
        rest    = command[17:].strip()
        parts   = rest.split(" at ", 1)
        role    = parts[0].strip()
        company = parts[1].strip() if len(parts) > 1 else "the company"
        from platforms.job_desc_parser import (
            generate_cover_letter, generate_email, _print_results
        )
        details = {"role": role, "company": company, "skills": [], "raw": ""}
        _print_results(details, generate_cover_letter(details), generate_email(details))
        return True

    if cmd.startswith("write cover letter "):
        rest    = command[19:].strip().split(" ", 1)
        role    = rest[0]
        company = rest[1] if len(rest) > 1 else "the company"
        from platforms.job_search_agent import generate_cover_letter
        generate_cover_letter(role, company)
        return True

    if cmd.startswith("draft email "):
        rest    = command[12:].strip().split(" ", 2)
        to      = rest[0] if rest else ""
        role    = rest[1] if len(rest) > 1 else "Developer"
        company = rest[2] if len(rest) > 2 else "the company"
        from platforms.job_search_agent import draft_email
        draft_email(to, role, company)
        return True

    return False