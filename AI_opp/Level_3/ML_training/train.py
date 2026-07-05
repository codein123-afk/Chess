import chess.pgn
import chess
from stockfish import Stockfish
import csv
import sys
import shutil
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "Engine"))
import Minimax as MX
import os
import zstandard as zstd
import io

print("Current working directory:", os.getcwd())
print("Files here:", os.listdir())

piece_map = {
    chess.Piece(chess.PAWN, chess.WHITE): "P",
    chess.Piece(chess.KNIGHT, chess.WHITE): "H",
    chess.Piece(chess.BISHOP, chess.WHITE): "B",
    chess.Piece(chess.ROOK, chess.WHITE): "R",
    chess.Piece(chess.QUEEN, chess.WHITE): "Q",
    chess.Piece(chess.KING, chess.WHITE): "K",
    chess.Piece(chess.PAWN, chess.BLACK): "-P",
    chess.Piece(chess.KNIGHT, chess.BLACK): "-H",
    chess.Piece(chess.BISHOP, chess.BLACK): "-B",
    chess.Piece(chess.ROOK, chess.BLACK): "-R",
    chess.Piece(chess.QUEEN, chess.BLACK): "-Q",
    chess.Piece(chess.KING, chess.BLACK): "-K",
}

def convert_board(board):
    my_board = [["0"] * 8 for _ in range(8)]
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        my_board[row][col] = piece_map[piece]
    return my_board

stockfish = Stockfish(path="/Users/apple/Desktop/Code/Chess/ML/stockfish/stockfish-macos-m1-apple-silicon",depth=15)

games_processed = 0
positions_written = 0
    

with open("game.pgn.zst", "rb") as compressed, open("positions.csv", "w", newline="") as csv_file:
    dctx = zstd.ZstdDecompressor()
    stream = dctx.stream_reader(compressed)
    text_stream = io.TextIOWrapper(stream, encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow([
        "white_material",
        "black_material",
        "passed_pawn_white",
        "passed_pawn_black",
        "score_board",
        "pawn_structure",
        "king_safety_white",
        "king_safety_black",
        "white_bishop_pair",
        "black_bishop_pair",
        "white_check",
        "black_check",
        "white_castled",
        "black_castled",
        "target"])

    while True:
        game = chess.pgn.read_game(text_stream)
        if game is None:
            break
        if game.errors:
            continue

        board = game.board()
        ply = 0  # reset per game
        white_castled = False
        black_castled = False
        try:
            for move in game.mainline_moves():
                is_castle = board.is_castling(move)
                board.push(move)
                ply += 1
                if is_castle:
                    if board.turn == chess.BLACK:
                        white_castled = True
                    else:
                        black_castled = True

                if ply < 10:  # skip opening book positions
                    continue
                if ply % 2 != 0:
                    continue

                my_board = convert_board(board)
                features = MX.extract_features(my_board,white_castled,black_castled)

                stockfish.set_fen_position(board.fen())
                evaluation = stockfish.get_evaluation()

                if evaluation["type"] == "cp":
                    target = max(min(evaluation["value"] / 100, 10), -10)
                else:
                    # mate score — clamp to ±100
                    target = 100 if evaluation["value"] > 0 else -100

                writer.writerow([*features, target])
                positions_written += 1

        except Exception as e:
            print(f"Error in game {games_processed + 1} at ply {ply}: {e}, skipping.")

        games_processed += 1
        if games_processed % 500 == 0:
            csv_file.flush()

        if games_processed % 100 == 0:
            print(f"Games processed: {games_processed}, positions written: {positions_written}")

print(f"Done. {games_processed} games, {positions_written} positions written to positions.csv")