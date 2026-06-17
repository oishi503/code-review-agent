# 🤖 AI Code Review Agent

An intelligent GitHub bot that automatically reviews Pull Requests using AI. Built with Python, FastAPI, and Groq (LLaMA 3.3 70B).

## 🎯 What it does

- Listens for GitHub Pull Request events via webhooks
- Parses the code diff to extract changed lines with line numbers
- Sends changed code to Groq AI (LLaMA 3.3 70B) for intelligent review
- Posts a structured review summary directly on the PR with severity ratings

## 🔍 Example Output

The bot automatically posts a comment like this on every PR:

### 🤖 AI Code Review Summary
**Total issues found: 4**

| Severity | Count |
|----------|-------|
| 🔴 High  | 1 |
| 🟡 Medium | 2 |
| 🟢 Low   | 1 |

## 🛠️ Tech Stack

- **Python** — core language
- **FastAPI** — webhook server
- **Groq API** — AI inference (LLaMA 3.3 70B)
- **GitHub Apps API** — PR event handling and comment posting
- **Cloudflare Tunnel** — exposes local server to GitHub webhooks

## 📁 Project Structure
