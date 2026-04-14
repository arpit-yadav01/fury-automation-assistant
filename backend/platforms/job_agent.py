# agents/platforms/job_agent.py
# STEP 137 — Job application agent
#
# Applies to jobs on any platform:
#   naukri, indeed, internshala, linkedin, monster, unstop, wellfound
#
# Uses personal_profile.py for all form data —
# name, email, phone, skills, resume, cover letter.
#
# Usage:
#   from agents.platforms.job_agent import apply_to_job
#   apply_to_job("react developer", platform="naukri")
#   apply_to_job("https://www.naukri.com/job-listings/...")
#   apply_to_job("full stack developer", platform="internshala")

import os
import re
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# PLATFORM SEARCH URLS
# -------------------------

SEARCH_URLS = {
    "naukri":      "https://www.naukri.com/{query}-jobs",
    "indeed":      "https://www.indeed.com/jobs?q={query}&l=India",
    "internshala": "https://internshala.com/internships/{query}-internship",
    "linkedin":    "https://www.linkedin.com/jobs/search/?keywords={query}",
    "monster":     "https://www.monster.com/jobs/search?q={query}&where=India",
    "unstop":      "https://unstop.com/jobs?searchTerm={query}",
    "wellfound":   "https://wellfound.com/jobs?q={query}",
}


# -------------------------
# DETECT PLATFORM FROM URL/INPUT
# -------------------------

def _detect_platform(input_str):
    """Detect which platform from URL or context."""
    s = input_str.lower()
    for platform in SEARCH_URLS.keys():
        if platform in s:
            return platform
    return None


def _is_url(s):
    return s.startswith("http://") or s.startswith("https://")


# -------------------------
# MAIN ENTRY POINT
# -------------------------

def apply_to_job(input_str, platform=None, role=None):
    """
    Apply to a job.

    Args:
        input_str: job URL, search query, or job description
        platform: force a specific platform (optional)
        role: job role to target (optional, uses profile default)

    Returns:
        visual agent result dict
    """
    from execution.visual_agent import run_visual_goal
    from brain.personal_profile import profile
    from brain.tab_intelligence import navigate_to_platform

    # detect platform
    if not platform:
        platform = _detect_platform(input_str)
    if not platform:
        platform = "naukri"  # default for India

    print(f"\n💼 Job Agent: {input_str}")
    print(f"   Platform: {platform}")

    # load personal context
    target_role = role or _extract_role(input_str) or profile.target_roles[0]
    ctx = profile.get_form_context(
        platform=platform,
        role=target_role,
        company=_extract_company(input_str)
    )

    # navigate to platform
    navigate_to_platform(platform)

    # build goal
    goal = _build_goal(input_str, platform, target_role, ctx)

    print(f"   Goal: {goal}")
    print(f"   Applying as: {profile.name} ({profile.email})")

    result = run_visual_goal(goal, context=ctx, max_steps=30)
    return result


def search_jobs(query, platform="naukri"):
    """
    Search for jobs matching a query on a platform.
    Opens results but doesn't apply — lets you review first.
    """
    from execution.visual_agent import run_visual_goal
    from brain.tab_intelligence import navigate_to_platform

    encoded = query.replace(" ", "-").lower()
    url = SEARCH_URLS.get(platform, "").replace("{query}", encoded)

    if not url:
        url = f"https://www.{platform}.com/jobs?q={query.replace(' ', '+')}"

    print(f"\n🔍 Searching {platform} for: {query}")
    navigate_to_platform(platform)

    goal = f"search for {query} jobs on {platform} and show the results"
    result = run_visual_goal(goal, max_steps=10)
    return result


# -------------------------
# GOAL BUILDER
# -------------------------

def _build_goal(input_str, platform, role, ctx):
    """Build a specific visual agent goal for job application."""

    if _is_url(input_str):
        return (
            f"go to {input_str}, "
            f"find the apply button, click it, "
            f"fill in name '{ctx['name']}', "
            f"email '{ctx['email']}', "
            f"phone '{ctx['phone']}', "
            f"submit the application"
        )

    return (
        f"on {platform} search for '{role}' jobs in India, "
        f"open the first relevant result, "
        f"click apply, "
        f"fill in name '{ctx['name']}', "
        f"email '{ctx['email']}', "
        f"phone '{ctx['phone']}', "
        f"and submit the application"
    )


# -------------------------
# HELPERS
# -------------------------

def _extract_role(input_str):
    """Try to extract a job role from the input string."""
    role_keywords = [
        "react", "node", "mern", "fullstack", "full stack",
        "frontend", "backend", "javascript", "python",
        "developer", "engineer", "intern"
    ]
    s = input_str.lower()
    for kw in role_keywords:
        if kw in s:
            # grab surrounding words
            words = s.split()
            for i, w in enumerate(words):
                if kw in w:
                    start = max(0, i - 1)
                    end = min(len(words), i + 2)
                    return " ".join(words[start:end])
    return None


def _extract_company(input_str):
    """Try to extract company name from URL."""
    if "naukri.com" in input_str:
        return "Naukri listing"
    if "indeed.com" in input_str:
        return "Indeed listing"
    if "linkedin.com" in input_str:
        return "LinkedIn listing"
    return ""


# -------------------------
# BULK APPLY (advanced)
# Apply to multiple jobs from a search
# -------------------------

def bulk_apply(role, platforms=None, max_jobs=3):
    """
    Search and apply to multiple jobs across platforms.

    Args:
        role: job role to search for
        platforms: list of platforms, defaults to ["naukri", "internshala"]
        max_jobs: max applications to submit
    """
    if not platforms:
        platforms = ["naukri", "internshala"]

    print(f"\n🚀 Bulk apply: {role} across {platforms}")
    results = []

    for platform in platforms:
        if len(results) >= max_jobs:
            break

        print(f"\n--- Trying {platform} ---")
        result = apply_to_job(role, platform=platform)
        results.append({
            "platform": platform,
            "outcome": result.get("outcome"),
            "steps": result.get("steps")
        })

        if result.get("outcome") == "success":
            print(f"✅ Applied on {platform}")
        else:
            print(f"❌ Failed on {platform}")

    # summary
    success_count = sum(1 for r in results if r["outcome"] == "success")
    print(f"\n📊 Applied: {success_count}/{len(results)} successful")
    return results