## Chess LLM:
This is an LLM-Powered chess analysis tool that analyses a game flags any mistakes, and then explains them. It is built in 2 versions, V1 being a straightforward pipeline with an API call, and V2 being a tool-calling agent that investigates positions independently rather than just using data it is given initially.

## How it works:
1. Parse PGN and step through each move in the game.
2. Stockfish analyses every position.
3. Flags when a mistake or blunder is made by the player we are analysing (when the evaluation swings past a threshold).
4. (V1) LLM explains why the move was a mistake, given the position, evaluation, the top line of the engine, and the line after the blunder.
4. (V2) Then LLM is given a consult_engine tool

## Setup:
- Requires Python 3.12+, Stockfish (install separately from stockfishchess.org)
- pip install -r requirements.txt
- Add API key to .env (see .env.example)
- There is an example game PGN already in the folder, but it is possible to upload a different game and use that instead.

## Evaluation:
I tested both versions on lots of different types of mistakes from different games. V1 correctly distinguished between missed opportunities and blunders, and was particularly successful in spotting tactical blunders/misses (when a short, forced sequence of moves leads to a better position). This is because these forcing lines are clearly reflected in the engine lines that we parse into the LLM. 

For positional mistakes, (when there is an error in spotting the best long term plans), the V1 was less able to describe the concept behind the mistake, partly because of the depth of the engine not being high enough (so the LLM couldn't see far enough into the future), but mainly because we only gave the LLM the top line of the engine, which doesn't show why other possibilities are inferior. For example, a positional mistake might force you to create weaknesses elsewhere to compensate for that mistake. Since the computer line doesn't show the LLM why these other weaknesses were actually forced. V2 was a lot better at spotting positional mistakes, as it could follow the what happens as the game progresses and with more branches to see why certain structures/piece coordinations might be good or bad.

Additionally, both versions occasionally struggled in the early game, because there are theoretical moves that exist that Stockfish incorrectly thinks are mistakes on a low depth, but are actually good moves on a much higher depth. This problem could be solved by either using a higher depth, or maybe by adding an opening database to the program.

Overall, this project was successful, especially in identifying tactical mistakes, but it had limited accuracy due to Stockfish's depth and using only one engine line. If multiple engine lines and a higher depth were used, as well as potentially using an opening database, it would improve the ability of the program to explain deeper positional mistakes.

## Potential extensions:
- Connect to an opening database, and query the database for any opening mistakes that are flagged that might not actually be mistakes.
