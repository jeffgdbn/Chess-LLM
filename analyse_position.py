import chess
import chess.engine

stockfish_path = "stockfish/stockfish-macos-m1-apple-silicon"


def analyse_position(fen, depth=15, linedepth=5, moves=None, engine_path=stockfish_path):
    board = chess.Board(fen)

    for move_index, uci_move in enumerate(moves or []):
        try:
            board.push_uci(uci_move)
        except (chess.IllegalMoveError, chess.InvalidMoveError, ValueError) as error:
            return {
                "error": (
                    f"Illegal move at index {move_index}: "
                    f"{uci_move!r} ({error})"
                )
            }

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))

    score = info.get("score")
    if score is None:
        raise ValueError(f"No engine evaluation available for FEN: {fen}")

    evaluation = score.relative.score(mate_score=10000) / 100
    principal_variation = info.get("pv", [])
    best_line = [move.uci() for move in principal_variation[:linedepth]]
    best_move = best_line[0] if best_line else None

    return {
        "evaluation": evaluation,
        "best_move": best_move,
        "best_line": best_line,
    }

    def consult_engine(fen, depth=15, moves=None, engine_path=stockfish_path):
        return analyse_position(fen, depth=depth, linedepth=1, moves=moves, engine_path=engine_path)