import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def post_comments(repo_name, pr_number, comments):
    if not comments:
        print("No issues found — nothing to post!")
        return

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    summary = build_summary(comments)
    
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    
    response = requests.post(url, headers=headers, json={"body": summary})
    
    if response.status_code == 201:
        print(f"Successfully posted review summary to PR!")
    else:
        print(f"Failed to post: {response.status_code} - {response.text}")

def build_summary(comments):
    high = len([c for c in comments if c.get("severity") == "high"])
    medium = len([c for c in comments if c.get("severity") == "medium"])
    low = len([c for c in comments if c.get("severity") == "low"])
    total = len(comments)

    summary = f"""## 🤖 AI Code Review Summary

**Total issues found: {total}**

| Severity | Count |
|----------|-------|
| 🔴 High  | {high} |
| 🟡 Medium | {medium} |
| 🟢 Low   | {low} |

### Issues found:

"""
    for comment in comments:
        severity = comment.get("severity", "low")
        emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(severity, "🟢")
        summary += f"- {emoji} **{comment.get('filename')}** line {comment.get('line_number')}: {comment.get('comment')}\n"

    return summary