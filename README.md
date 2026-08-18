## What it does:
This chess coach uses stockfish to find mistakes in a pgn file for a chess game, and parses these into an LLM, to explain for each mistake why it was a mistake, and what a better alternative move would be.

## How it works:
1. Parse pgn and step through each move in the game.
2. Stockfish analyses every position.
3. Flags when a mistake is made by the player we are analysing (when the evaluation swings past a threshold).
4. LLM explains why the move was a mistake, given the position, evaluation, the top line of the engine, and the line after the blunder.

## Setup:
- Requires Python 3.12+, Stockfish (install separately from stockfishchess.org)
- pip install -r requirements.txt
- Add API key to .env (see .env.example)
- There is an example game pgn already in the folder, but it is possible to upload a different game and use that instead.

## Evaluation:
I tested the system on lots of different types of mistakes from different games. The LLM correctly distinguished between missed opportunities and blunders, and was particularly successful in spotting tactical blunders/misses (when a short, forced sequence of moves leads to a better position). This is because these forcing lines are clearly reflected in the engine lines that we parse into the LLM. 

For positional mistakes, (when there is an error in spotting the best long term plans), the LLM was  less able to describe the concept behind the mistake, partly because of the depth of the engine not being high enough (so the LLM couldn't see far enough into the future), but mainly because we only gave the LLM the top line of the engine, which doesn't show why other possibilities are inferior. For example, a positional mistake might force you to create weaknesses elsewhere to compensate for that mistake. Since in the computer line doesn't show the LLM why these other weaknesses were actually forced.

Additionally, the LLM occasionally struggled in the early game, because there are theoretical moves that exist that stockfish incorrectly thinks are mistakes on a low depth, but are actually good moves on a much higher depth. This problem could be solved by either using a higher depth, or maybe by adding an opening database to the program.

Overall, this project was successful, especially in identifying tactical mistakes, but it had limited accuracy due to stockfish's depth and using only one engine line. If multiple engine lines and a higher depth were used, as well as potentially using an opening database, it would improve the ability of the program to explain deeper positional mistakes.

## Potential extensions:
- Connect to an opening database, and query the database for any opening mistakes that are flagged that might not actually be mistakes.
- Give the LLM the option to consult stockfish, so it can find out itself why other moves weren't the best move, giving it a broader picture of why the mistake was a mistake.
