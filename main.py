import hmac
import hashlib
import os
import requests
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from diff_parser import parse_diff
from reviewer import review_diff
from github_poster import post_comments

load_dotenv()

app = FastAPI()

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def verify_signature(payload: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def fetch_diff(url: str) -> str:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.diff"
    }
    response = requests.get(url, headers=headers)
    return response.text


@app.get("/")
def home():
    return {"status": "Code Review Agent is running!"}


@app.post("/webhook")
async def webhook(request: Request):
    payload_bytes = await request.body()

    signature = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(payload_bytes, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()

    action = payload.get("action")
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored"}

    pr_number = payload["pull_request"]["number"]
    repo_name = payload["repository"]["full_name"]
    diff_url = payload["pull_request"]["diff_url"]

    print(f"\n--- New PR #{pr_number} in {repo_name} ---")
    print(f"Fetching diff from {diff_url}...")

    diff_text = fetch_diff(diff_url)
    print(f"Diff fetched! Parsing...")

    parsed = parse_diff(diff_text)
    print(f"Parsed {len(parsed)} files. Sending to Gemini for review...")

    comments = review_diff(parsed)
    print(f"Gemini found {len(comments)} issues. Posting to GitHub...")

    post_comments(repo_name, pr_number, comments)
    print(f"Done!")

    return {"status": "ok", "issues_found": len(comments)}