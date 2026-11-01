from fastapi import APIRouter, HTTPException
from models import GameAnalysisRequest
from services.chess_service import analyze_and_validate_pgn
from services.chess_service import analyze_with_stockfish

router = APIRouter(prefix="/partidas", tags=["Partidas"])

@router.post("/analisar", summary="Recebe a string PGN de uma partida de xadrez, analisa e valida a partida " \
"e retorna os detalhes da partida e o FEN final.")
def analyze_game(request: GameAnalysisRequest):
    if not request.pgn.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do PGN não pode estar vazio.")

    try:
        resultado_analise = analyze_and_validate_pgn(request.pgn)

        fen_atual = resultado_analise["fen_final"]
        analise_stockfish = analyze_with_stockfish(fen_atual)

        return{
            "status": "sucesso",
            "cor": request.cor_jogador,
            **resultado_analise,
            "stockfish": analise_stockfish,
            "mensagem": "Partida validada com sucesso pelo serviço de stockfish."
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))