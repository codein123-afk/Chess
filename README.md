# Chess Engine

A chess engine built completely from scratch using Python and Pygame. The project implements all standard chess rules and includes three AI difficulty levels, ranging from a random move generator to an alpha-beta search engine with a Stockfish-trained evaluation function.

The project started as a way to understand how chess engines work and gradually evolved into a complete implementation covering move generation, search algorithms, evaluation functions, and machine learning.


# Features

* Complete chess rules implementation
    * Legal move generation
    * Castling
    * Pawn promotion
    * Check, checkmate, and stalemate detection
* Three AI difficulty levels
* Alpha-beta search with several common engine optimizations
* Evaluation function based on both material and positional features
* Dataset generation using real PGN games and Stockfish evaluations
* Linear regression model for learning evaluation weights

```
chess-engine-project/
├── two_player/
│   └── two_player_game.py
│
├── ai_opponent/
│   ├── level_1_random/
│   │   └── random_ai.py
│   │
│   ├── level_2_heuristic/
│   │   ├── capture_priority_ai.py
│   │   └── max_material_ai.py
│   │
│   └── level_3_search_engine/
│       ├── Minimax.py
│       └── ML_training/
│           ├── train.py  # Converts PGN games into a CSV dataset of extracted features and Stockfish evaluations.
│           ├── train_evaluator.py  # contains all data from csv and trains a linear regression model on it 
│           ├── game.pgn.zst # contains all position used for training
│           └── position.csv # contains all of result of all games used for training
│
├── assets/
│   └── Images/
│
└── README.md
```

# Running the Project

Clone the repository and install the required packages.

```
git clone <your-repo-url>
cd chess-engine-project
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Run any of the following game modes:
```
python two_player/two_player_game.py
python ai_opponent/level_1_random/random_ai.py
python ai_opponent/level_2_heuristic/capture_priority_ai.py
python ai_opponent/level_2_heuristic/max_material_ai.py
python ai_opponent/level_3_search_engine/engine.py
```
Click on a piece to see its legal moves and click on a highlighted square to make the move. Pawn promotion is handled through an on-screen selection menu.

# AI Difficulty Levels


## Level 1 – Random


The simplest opponent. It generates every legal move and chooses one at random.

Although it doesn’t play strategically, it is useful for testing move generation and serves as an easy opponent.

## Level 2 – Heuristic


This level contains two simple chess-playing strategies.

Capture Priority

If a capture is available, the AI captures the most valuable opponent piece. Otherwise, it plays a random legal move.

Max Material

Every legal move is evaluated using material count, and the move resulting in the highest material advantage is selected.

These heuristics play noticeably better than random but cannot look ahead, making them vulnerable to tactical ideas such as forks and sacrifices.



## Level 3 – Search Engine


The strongest engine in the project.

It uses Minimax with Alpha-Beta Pruning to search multiple moves ahead while reducing the number of positions that need to be evaluated.

Additional optimizations include:

* Iterative Deepening
* Move Ordering
* Killer Move Heuristic
* Transposition Tables
* Zobrist Hashing
* Quiescence Search

Instead of evaluating only material, the engine also considers positional factors such as:

* Piece-square tables
* Passed pawns
* Doubled and isolated pawns
* King safety
* Bishop pair bonus
* Endgame king positioning


# Training the Evaluation Function

The project also includes a simple machine learning pipeline for learning evaluation weights.

* Minimax.py contains the extract_features() function, which extracts the same positional features used by the engine’s evaluation function. These features are used to create the training dataset.
* game.pgn.zst contains the collection of chess games used for training. Each game is replayed move by move to generate board positions.
* train.py replays every game in game.pgn.zst, calls extract_features() from Minimax.py for each position, and uses Stockfish to generate an evaluation score. The extracted features and Stockfish evaluations are then stored as a labeled dataset, which is used to train a linear regression model for the evaluation function.
* train_evaluator.py trains a linear regression model on this dataset to learn evaluation weights automatically.

# Technologies Used

* Python
* Pygame
* python-chess
* Stockfish
* pandas
* scikit-learn
* joblib
* zstandard

# Future Improvements

Some ideas for extending the project:

* Integrate the learned evaluation weights directly into the engine.
* Compare the learned evaluator against the manually tuned evaluator by making them play against each other.
* Add a menu to choose AI difficulty from a single launcher.
* Add Perft tests for validating move generation.
* Experiment with a small neural-network evaluation function.

# Notes

The repository was reorganized from several experimental scripts into the current project structure. Shared assets were consolidated into a single directory, hardcoded file paths were removed, and the training scripts were updated to work across different systems.

There is currently one known issue: generate_dataset.py and engine.py use different versions of the extract_features() function. This needs to be reconciled before generating a new training dataset.


# Requiremnet 
pygame==2.6.1 numpy==2.3.5
