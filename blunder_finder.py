
import chess
import chess.pgn

from analyse_position import analyse_position


def blunder_finder(
    chosen_colour="white",
    pgn_path="lichess_pgn_2024.08.16_winifyoucan1266_vs_jefgdbn.Bsm6WW23.pgn",
    eval_threshold=1,
    depth=12,
    linedepth=5,
    engine_path="stockfish/stockfish-macos-m1-apple-silicon",
):
    colour = chess.WHITE if chosen_colour == "white" else chess.BLACK
    # open the PGN
    with open(pgn_path, "r", encoding="utf-8") as f:
        game = chess.pgn.read_game(f)

    if game is None:
        raise ValueError("No game found in PGN file.")

    board = game.board()

    blunders = []
    moves_for_side = 0

    previous_analysis = analyse_position(
        board.fen(), depth=depth, linedepth=linedepth, engine_path=engine_path
    )
    previous_eval = previous_analysis["evaluation"]
    previous_line = previous_analysis["best_line"]

    for move in game.mainline_moves():
        fen = board.fen()
        board.push(move)

        current_analysis = analyse_position(
            board.fen(), depth=depth, linedepth=linedepth, engine_path=engine_path
        )
        current_eval = current_analysis["evaluation"]
        engine_line = current_analysis["best_line"]

        if board.turn == colour:
            moves_for_side += 1
            eval_swing = abs(previous_eval - current_eval)

            if eval_swing > eval_threshold:
                blunders.append({
                    "move_number": moves_for_side,
                    "eval_before": round(previous_eval, 2),
                    "eval_after": round(current_eval, 2),
                    "engine_line_after_blunder": [move.uci()] + engine_line,
                    "best_move_line": previous_line,
                    "fen": fen,
                    "best_move": current_analysis["best_move"],
                })

        previous_line = engine_line
        previous_eval = current_eval

    return blunders
