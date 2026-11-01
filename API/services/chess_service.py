import io
import chess
import chess.pgn
import chess.engine
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOCKFISH_PATH = os.path.join(BASE_DIR, "..", "engine", "stockfish.exe")

def analyze_and_validate_pgn(pgn_string: str) -> dict:
    """
    Recebe a string PGN de uma partida de xadrez, analisa e valida a partida
    e retorna os detalhes da partida e o FEN final.
    """
    pgn_io = io.StringIO(pgn_string)
    partida = chess.pgn.read_game(pgn_io)

    if partida is None:
        raise ValueError("Não foi possível ler o PGN enviado. Formato inválido.")

    tabuleiro = partida.board()
    lances_validados = []

    for lance in partida.mainline_moves():
        lances_validados.append(tabuleiro.san(lance))
        tabuleiro.push(lance)

    return {
        "total_lances": len(lances_validados),
        "lances": lances_validados,
        "fen_final": tabuleiro.fen()
    }

def analyze_with_stockfish(fen: str, depth: int = 15) -> dict:
    """
    Recebe uma string FEN, inicializa o Stockfish e retorna a avaliação e o melhor lance.
    """
    if not os.path.exists(STOCKFISH_PATH):
        return {"erro": f"Executavel do Stockfish não encontrado em {STOCKFISH_PATH}"}

    try:
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            board = chess.Board(fen)

            limit = chess.engine.Limit(time=0.1)
            info = engine.analyse(board, limit)

            score = info["score"].white().score(mate_score=10000)

            result = engine.play(board, limit)
            best_move = result.move

            return{
                "avaliacao_centipawns": score,
                "melhor_lance": board.san(best_move) if best_move else None
            }
    except Exception as e:
        return {"erro": str(e)}