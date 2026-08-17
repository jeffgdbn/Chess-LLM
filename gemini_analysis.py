from dotenv import load_dotenv
load_dotenv()

import os
from google import genai

from blunder_finder import blunder_finder

chosen_colour = "white"
pgn_path = "lichess_pgn_2024.08.16_winifyoucan1266_vs_jefgdbn.Bsm6WW23.pgn"
eval_threshold = 1
depth = 12
print(f"Analyzing game {pgn_path} for {chosen_colour} with eval threshold {eval_threshold} and depth {depth}...")   
blunders = blunder_finder(chosen_colour, pgn_path, eval_threshold, depth)

print(f"Found {len(blunders)} blunders for {chosen_colour} in the game {pgn_path} with eval threshold {eval_threshold} and depth {depth}.")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = "For each of these blunders, provide a short explaination why they are a mistake and what the better plan was"
for blunder in blunders:
    prompt += f"Move {blunder['move_number']}: Eval before: {blunder['eval_before']}, Eval after: {blunder['eval_after']}, Engine line after blunder: {blunder['engine_line_after_blunder']}, Best move line: {blunder['best_move_line']}, FEN: {blunder['fen']}\n"
print(prompt)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print(response.text)