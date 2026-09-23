from dotenv import load_dotenv
load_dotenv()

from blunder_finder import blunder_finder
from chess_agent import explain_blunder_with_gemini

STOCKFISH_PATH = "stockfish/stockfish-macos-m1-apple-silicon"


def main():
    pgn_path = "lichess_pgn_2024.08.16_winifyoucan1266_vs_jefgdbn.Bsm6WW23.pgn"

    blunders = blunder_finder(
        chosen_colour="white",
        pgn_path=pgn_path,
        eval_threshold=1,
        depth=12,
        linedepth=5,
        engine_path=STOCKFISH_PATH,
    )
    print(f"Found {len(blunders)} flagged mistakes.\n")

    for blunder in blunders:
        move_played = blunder["engine_line_after_blunder"][0]
        print(f"Move: {move_played}")
        explanation = explain_blunder_with_gemini(
            blunder["fen"],
            move_played,
            player_to_move="white",
            depth=15,
            linedepth=5,
        )
        print(explanation)
        print("-" * 40)


if __name__ == "__main__":
    main()