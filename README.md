What it does:

This chess coach uses stockfish to find blunders in a pgn file for a chess game, and parses these into an LLM, to explain for each blunder why it was a mistake, and what a better alternative would be.

How it works:
1. Parse pgn and step through each move in the game.
2. Stockfish analyses every position.
3. Flags when a blunder is made by the player we are analysing (when the evaluation swings past a threshold).
4. LLM explains why the move was a blunder, given the position, evaluation, the top line of the engine, and the line after the blunder.

## Setup
- Requires Python 3.12+, Stockfish (install separately from stockfishchess.org)
- pip install -r requirements.txt
- Add API keys to .env (see .env.example)
