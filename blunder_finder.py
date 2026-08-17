
import chess
import chess.pgn
import chess.engine

def blunder_finder(chosen_colour="white", pgn_path="lichess_pgn_2024.08.16_winifyoucan1266_vs_jefgdbn.Bsm6WW23.pgn", eval_threshold=1, depth=12, engine_path="stockfish/stockfish-macos-m1-apple-silicon"):
    colour = chess.WHITE if chosen_colour == "white" else chess.BLACK
    # open the PGN
    with open(pgn_path, "r", encoding="utf-8") as f:
        game = chess.pgn.read_game(f)

    if game is None:
        raise ValueError("No game found in PGN file.")

    board = game.board()

    def score_to_float(score):
        if score.is_mate():
            return 10000 if score.mate() > 0 else -10000
        return score.score(mate_score=100000) / 100.0

    blunders = []
    moves_for_side = 0
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        previous_eval = score_to_float(
            engine.analyse(board, chess.engine.Limit(depth=depth))["score"].pov(colour)
        )
        info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=3)
        previous_line = [m.uci() for m in info[0]["pv"]] if "pv" in info[0] else []
        for move in game.mainline_moves():
            fen = board.fen()
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=3)
            engine_line = [m.uci() for m in info[0]["pv"]] if "pv" in info[0] else []
            current_score = info[0]["score"].pov(colour)
            current_eval = score_to_float(current_score)

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
                        "fen": fen
                    })

            previous_line = engine_line
            previous_eval = current_eval

    return blunders
