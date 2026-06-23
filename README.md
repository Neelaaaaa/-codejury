# CodeJury 🧑‍⚖️

A multi-agent AI system that debugs competitive programming code by having three AI agents collaborate, critique, and reach a final verdict — instead of relying on a single AI call.

## How it works

Most "AI code reviewer" tools just send your code to one model and print whatever it says. CodeJury instead uses **three agents with different roles**, each one building on the last:

1. **Agent 1 — The Guesser**: Analyzes the problem and code, proposes a diagnosis and fix.
2. **Agent 2 — The Doubter**: Reviews Agent 1's reasoning critically — confirms it, challenges it, or improves on it. Does not blindly trust the first answer.
3. **Agent 3 — The Judge**: Reads both opinions and produces one final, clean, structured verdict with the bug location, explanation, and fixed code.

This mimics how real code review works on engineering teams — one person proposes a fix, another double-checks it, and a final decision is made.

## Example

**Problem:** Implement binary search on a sorted array.

**Buggy code:**

    def binary_search(arr, target):
        left = 0
        right = len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid
            else:
                right = mid
        return -1

**CodeJury's verdict:**

    BUG FOUND: Yes
    LOCATION: left = mid
    EXPLANATION: When the search range narrows to a single element, mid evaluates to left.
    Setting left = mid fails to shrink the search space, causing an infinite loop.
    FIXED CODE: [corrected version provided]

## Tech Stack

- Python
- Google Gemini API (`google-genai`)
- python-dotenv (for secure API key handling)

## Why I built this

I wanted to go beyond a basic "wrap an API call" AI project and explore **multi-agent systems** — where multiple AI agents with distinct roles collaborate to produce a more reliable answer than any single model call. I chose competitive programming bugs as the domain since it's an area I'm personally strong in (DSA), which let me properly evaluate whether the agents' reasoning was actually correct.

## Key engineering decisions

- **Retry logic**: Handles API rate limits / server errors gracefully with automatic retries instead of crashing.
- **Structured prompting**: Forces each agent into a consistent output format, preventing rambling, inconsistent answers.
- **Secure key handling**: API keys are stored in a local `.env` file (excluded from version control via `.gitignore`), never hardcoded.

## How to run it

1. Clone this repo
2. Install dependencies:

       pip install google-genai python-dotenv

3. Create a `.env` file with your own Gemini API key:

       GEMINI_API_KEY=your_key_here

4. Put your problem statement in `problem.txt` and buggy code in `code.txt`
5. Run:

       python codejury.py

## Future improvements

- Web interface instead of text files
- Automatically run the fixed code against test cases to verify correctness
- Support for multiple programming languages
