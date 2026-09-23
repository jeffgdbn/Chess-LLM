import os

from dotenv import load_dotenv
from google import genai

from analyse_position import analyse_position

load_dotenv()

def explain_blunder_with_gemini(
    fen,
    move,
    player_to_move="white",
    api_key=None,
    depth=15,
    linedepth=5,
    model="gemini-3.6-flash",
):

    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    position = analyse_position(fen, depth=depth, linedepth=linedepth, moves=[move])
    engine_error = position.get("error")
    evaluation = position.get("evaluation")
    best_line = position.get("best_line", [])
    best_move = best_line[0] if best_line else None

    client = genai.Client(api_key=api_key)

    prompt = (
        "You are a chess coach. Use the consult_engine tool when you need "
        "Stockfish evidence for the position or for a candidate line. "
        "Do not guess the evaluation from memory.\n\n"
        "You are given an attempted move from the user and an engine/analysis "
        "wrapper that can report whether the move was legal in the supplied "
        "position. If that wrapper reports an engine-side error, include it "
        "in your reasoning and let the model decide how to handle the illegal "
        "or malformed move before continuing.\n\n"
        f"The attempted move is: {move}\n"
        f"FEN: {fen}\n"
        f"Player to move: {player_to_move}\n"
        f"Engine move-request status: {engine_error or 'Move was legal.'}\n"
        f"Stockfish evaluation from analyse_position: {evaluation}\n"
        f"Stockfish best move from analyse_position: {best_move}\n\n"
        "Give a brief but clear explanation in plain English.\n"
        "Please explain:\n"
        "- whether the move is a mistake or blunder\n"
        "- why it is bad in this position\n"
        "- what the stronger move or plan is\n"
        "- how the evaluation changes and what tactical or strategic issue is involved\n"
        "Keep it concise but informative, and do not mention the engine by name unless useful."
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text

