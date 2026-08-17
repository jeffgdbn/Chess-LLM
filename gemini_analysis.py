import os
from dotenv import load_dotenv
from google import genai

from blunder_finder import blunder_finder

load_dotenv()

# Get settings from the user
pgn_path = input("Enter the path to the PGN file: ")
chosen_colour = input("Which colour do you want to analyze? (white/black): ").lower()

eval_threshold = 1
depth = 12

print(
    f"\nAnalyzing game {pgn_path} for {chosen_colour} "
    f"with eval threshold {eval_threshold} and depth {depth}..."
)

blunders = blunder_finder(
    chosen_colour,
    pgn_path,
    eval_threshold,
    depth
)

print(
    f"Found {len(blunders)} blunders for {chosen_colour} "
    f"in the game {pgn_path} with eval threshold "
    f"{eval_threshold} and depth {depth}."
)

# Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)

prompt = """
For each of these blunders, provide a short explanation of:
- why the move was a mistake
- what the better plan was

Explain the ideas in a way that a chess player can understand.

"""

for blunder in blunders:
    prompt += (
        f"Move {blunder['move_number']}: "
        f"Eval before: {blunder['eval_before']}, "
        f"Eval after: {blunder['eval_after']}, "
        f"Engine line after blunder: {blunder['engine_line_after_blunder']}, "
        f"Best move line: {blunder['best_move_line']}, "
        f"FEN: {blunder['fen']}\n"
    )

print("\nGenerating explanations...\n")

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print(response.text)