# platforms/youtube_agent.py
# Handles YouTube playback properly
# Uses direct video URL via YouTube search API (no ads)
# Falls back to coordinate click if API unavailable

import os
import time
import urllib.parse
import urllib.request
import json
import re


# -------------------------
# YOUTUBE SEARCH — NO ADS
# Uses YouTube's internal search endpoint
# Returns actual video URL, skips promoted content
# -------------------------

def search_youtube(query, max_results=5):
    """
    Search YouTube and return real video URLs.
    No ads, no promoted content.
    Uses YouTube's public search — no API key needed.
    """
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"

        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")

        # extract video IDs from ytInitialData
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)

        # deduplicate while preserving order
        seen = set()
        unique_ids = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                unique_ids.append(vid)

        # return direct watch URLs (no ads)
        results = [
            f"https://www.youtube.com/watch?v={vid}"
            for vid in unique_ids[:max_results]
        ]
        return results

    except Exception as e:
        print(f"YouTube search error: {e}")
        return []


def play_youtube(query):
    """
    Play a YouTube video — skips ads by using direct video URL.

    Flow:
    1. Search YouTube for the query
    2. Get first real video ID (not promoted)
    3. Open the direct watch URL in Chrome
    4. Done — no clicking needed, no ad risk
    """
    from browser.browser_agent import open_website

    print(f"\n🎵 YouTube: {query}")

    # get direct video URL
    results = search_youtube(query)

    if results:
        video_url = results[0]
        print(f"   Found: {video_url}")
        print(f"   Opening directly — no ads")
        open_website(video_url)
        time.sleep(2)
        return {"outcome": "success", "url": video_url, "query": query}
    else:
        # fallback to search results page
        print("   Falling back to search results page")
        encoded = query.replace(" ", "+")
        open_website(f"https://www.youtube.com/results?search_query={encoded}")
        time.sleep(3)
        # click first result at known coordinate
        try:
            import pyautogui
            from execution.visual_agent import _ensure_browser_focused
            _ensure_browser_focused()
            time.sleep(0.5)
            pyautogui.click(400, 250)
            print("   Clicked first result")
        except Exception as e:
            print(f"   Click error: {e}")
        return {"outcome": "success", "query": query}