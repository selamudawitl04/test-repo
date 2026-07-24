#!/usr/bin/env python3
"""
Free AI code review using Google Gemini API.
Reads PR diff and sends to Gemini for review, outputs comment-formatted result.
"""

import os
import sys
import json
import urllib.request
import urllib.error

def get_gemini_api_key():
    """Get Gemini API key from environment."""
    key = os.environ.get('GEMINI_API_KEY')
    if not key:
        print("ERROR: GEMINI_API_KEY environment variable not set")
        sys.exit(1)
    return key

def get_diff_from_env():
    """Get the PR diff from GITHUB_DIFF environment variable or git diff."""
    # GitHub Actions will pass the diff, or we read it from git
    diff = os.environ.get('GITHUB_DIFF', '')

    if not diff:
        # Fallback: try to get diff from git
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'diff', 'origin/main...HEAD'],
                capture_output=True,
                text=True,
                timeout=10
            )
            diff = result.stdout
            if not diff:
                # If that fails, try against master
                result = subprocess.run(
                    ['git', 'diff', 'origin/master...HEAD'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                diff = result.stdout
        except Exception as e:
            print(f"Warning: could not get diff from git: {e}")
            diff = "[No diff available]"

    return diff

def call_gemini_api(api_key, diff_content):
    """Call Gemini API with the diff and return review."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    review_prompt = f"""You are a professional code reviewer. Please review the following code diff and provide constructive feedback.

Focus on:
1. Security issues (XSS, SQL injection, etc.)
2. Accessibility issues (missing alt text, semantic HTML, etc.)
3. Performance problems
4. Code quality and best practices
5. Deprecated APIs or tags

Provide your review as a concise GitHub PR comment (use markdown formatting).

---
CODE DIFF:
{diff_content}
---

Please provide a professional but friendly review. If there are no issues, say so."""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": review_prompt
                    }
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    # Add API key to URL
    full_url = f"{url}?key={api_key}"

    try:
        req = urllib.request.Request(
            full_url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            response_data = json.loads(response.read().decode('utf-8'))

        # Extract the review text from response
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            candidate = response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                if len(candidate['content']['parts']) > 0:
                    review_text = candidate['content']['parts'][0].get('text', '')
                    return review_text

        return "ERROR: Could not extract review from API response"

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return f"ERROR: Gemini API call failed with status {e.code}: {error_body}"
    except urllib.error.URLError as e:
        return f"ERROR: Network error calling Gemini API: {e.reason}"
    except Exception as e:
        return f"ERROR: Unexpected error: {str(e)}"

def main():
    """Main entry point."""
    api_key = get_gemini_api_key()
    diff = get_diff_from_env()

    if not diff or diff == "[No diff available]":
        print("WARNING: No diff found. Skipping review.")
        # Write empty review so workflow doesn't fail
        with open('review_result.txt', 'w') as f:
            f.write("No changes detected in this PR.")
        return

    print("Calling Gemini API for code review...")
    review = call_gemini_api(api_key, diff)

    # Write review to file for workflow to post as comment
    with open('review_result.txt', 'w') as f:
        f.write(review)

    print("Review complete. Output written to review_result.txt")
    print("\n--- REVIEW ---")
    print(review)

if __name__ == '__main__':
    main()
