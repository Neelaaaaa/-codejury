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

# STEP A: Get Agent 1's opinion first (same as before)
agent1_prompt = f"""
You are an expert competitive programmer reviewing buggy code.

PROBLEM:
{problem}

CODE:
{buggy_code}

Your job: Find what is wrong with this code (if anything). Be specific - mention the exact line and why it's wrong. If you think it's actually correct, say so clearly.
"""

agent1_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=agent1_prompt
)

agent1_answer = agent1_response.text

print("=== AGENT 1 (The Guesser) says: ===")
print(agent1_answer)
print("\n")

# STEP B: Now Agent 2 reviews Agent 1's answer
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
"""

agent2_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=agent2_prompt
)

print("=== AGENT 2 (The Doubter) says: ===")
print(agent2_response.text)