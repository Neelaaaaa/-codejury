from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

problem = """
Given an array of integers, return the maximum sum of any contiguous subarray.
Example: [-2,1,-3,4,-1,2,1,-5,4] -> answer is 6 (subarray [4,-1,2,1])
"""

buggy_code = """
def max_subarray(nums):
    max_sum = 0
    current_sum = 0
    for num in nums:
        current_sum += num
        if current_sum > max_sum:
            max_sum = current_sum
        if current_sum < 0:
            current_sum = 0
    return max_sum
"""

# ---------- AGENT 1 ----------
agent1_prompt = f"""
You are an expert competitive programmer reviewing buggy code.

PROBLEM:
{problem}

CODE:
{buggy_code}

Your job: Find what is wrong with this code (if anything).

RULES (follow strictly):
- Give EXACTLY ONE diagnosis. Do not propose multiple alternative explanations.
- Give EXACTLY ONE fixed version of the code. Do not show "alternatively" or a second version.
- Do not change your mind mid-answer. Decide first, then explain clearly.
- Keep your total answer under 150 words, excluding the code block.

Format your answer as:
BUG: [one sentence]
WHY: [2-3 sentences max]
FIX:
[one clean code block]
"""

agent1_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=agent1_prompt
)
agent1_answer = agent1_response.text

print("=== AGENT 1 (The Guesser) says: ===")
print(agent1_answer)
print("\n")

# ---------- AGENT 2 ----------
agent2_prompt = f"""
You are a skeptical senior code reviewer. Another AI (Agent 1) just analyzed this code and gave an opinion.
Your job is NOT to trust it blindly. Check if Agent 1's reasoning is actually correct.

PROBLEM:
{problem}

CODE:
{buggy_code}

AGENT 1's OPINION:
{agent1_answer}

Your job:
1. Is Agent 1 correct? Say clearly: AGREE or DISAGREE.
2. If you disagree, explain exactly what Agent 1 got wrong.
3. If you agree, see if there's anything Agent 1 missed or could explain better.

Keep your total answer under 150 words.
"""

agent2_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=agent2_prompt
)
agent2_answer = agent2_response.text

print("=== AGENT 2 (The Doubter) says: ===")
print(agent2_answer)
print("\n")

# ---------- AGENT 3 ----------
agent3_prompt = f"""
You are the final judge in a code review process. Two other AI agents have given their opinions
about a piece of buggy code. Your job is to give ONE final, clear, concise verdict.

PROBLEM:
{problem}

CODE:
{buggy_code}

AGENT 1's OPINION:
{agent1_answer}

AGENT 2's OPINION (reviewing Agent 1):
{agent2_answer}

Your job: Give a final verdict in this EXACT format:

BUG FOUND: [Yes/No]
LOCATION: [exact line or "N/A"]
EXPLANATION: [2-3 sentences max, simple language]
FIXED CODE:
[Give ONLY ONE final, clean, working Python function. No comments explaining alternative approaches. No second versions. Just the one correct function, nothing else.]
"""

agent3_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=agent3_prompt
)

print("=== AGENT 3 (The Judge) — FINAL VERDICT: ===")
print(agent3_response.text)