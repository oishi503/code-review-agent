from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_diff(parsed_files):
    all_comments = []

    for file in parsed_files:
        filename = file['filename']

        for hunk in file['hunks']:
            lines = hunk['lines']
            if not lines:
                continue

            code_block = ""
            for line in lines:
                prefix = "+" if line['type'] == 'added' else "-"
                code_block += f"Line {line['line_number']}: {prefix} {line['content']}\n"

            prompt = f"""You are a senior software engineer doing a code review.

Analyze this code change from the file: {filename}

{code_block}

Find any of these issues:
- Bugs or logical errors
- Security vulnerabilities
- Bad practices
- Performance problems

Respond ONLY with a JSON array. Each issue should have exactly these fields:
- "filename": the file name
- "line_number": the line number as an integer
- "severity": either "high", "medium", or "low"
- "comment": a clear explanation of the issue and how to fix it

If there are no issues, respond with an empty array: []

Do not include any text outside the JSON array."""

            try:
                print(f"Sending {filename} to Groq for review...")
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                response_text = response.choices[0].message.content.strip()
                print(f"Groq response: {response_text[:100]}...")

                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]

                comments = json.loads(response_text)
                all_comments.extend(comments)
                print(f"Groq found {len(comments)} issues in {filename}")

            except Exception as e:
                print(f"Error reviewing {filename}: {e}")
                continue

    return all_comments