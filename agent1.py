from google import genai

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# This is the coding problem
problem = """
Given an array of integers, return the maximum sum of any contiguous subarray.
Example: [-2,1,-3,4,-1,2,1,-5,4] -> answer is 6 (subarray [4,-1,2,1])
"""

# This is the buggy code we want to check
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

# This is the instruction we give the AI - this turns it into "Agent 1"
prompt = f"""
You are an expert competitive programmer reviewing buggy code.

PROBLEM:
{problem}

CODE:
{buggy_code}

Your job: Find what is wrong with this code (if anything). Be specific - mention the exact line and why it's wrong. If you think it's actually correct, say so clearly.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)

print("=== AGENT 1 (The Guesser) says: ===")
print(response.text)