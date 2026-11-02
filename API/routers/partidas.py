from fastapi import APIRouter, HTTPException
from models import GameAnalysisRequest
from services.chess_service import analyze_and_validate_pgn, analyze_with_stockfish, analisar_partida_completa
from services.gemini_service import gerar_explicacao_jogada, gerar_resumo_partida

router = APIRouter(prefix="/partidas", tags=["Partidas"])

@router.post("/analisar", summary="Recebe a string PGN de uma partida de xadrez, analisa e valida a partida e retorna os detalhes da partida, o FEN final e a explicação da IA." )
def analyze_game(request: GameAnalysisRequest):
    if not request.pgn.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do PGN não pode estar vazio.")

    try:
        resultado_analise = analyze_and_validate_pgn(request.pgn)

        fen_atual = resultado_analise["fen_final"]
        analise_stockfish = analyze_with_stockfish(fen_atual)

        if "erro" in analise_stockfish:
            raise HTTPException(status_code=500, detail=analise_stockfish["erro"])

        melhor_lance = analise_stockfish.get("melhor_lance")
        avaliacao = analise_stockfish.get("avaliacao_centipawns")

        explicacao_ia = gerar_explicacao_jogada(
            fen=fen_atual, 
            melhor_lance = melhor_lance, 
            avaliacao = avaliacao
        )

        return{
            "status": "sucesso",
            "cor": request.cor_jogador,
            **resultado_analise,
            "stockfish": analise_stockfish,
            "ai_explicacao": explicacao_ia,
            "mensagem": "Partida validada e explicada com sucesso pelo Stockfish e Gemini."
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))

@router.post("/analisar-completa", summary="Analisa a partida de xadrez inteira lance por lance com Stockfish e gera um relatório geral com IA.")
def analyze_full_game(request: GameAnalysisRequest):
    if not request.pgn.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do PGN não pode estar vazio.")
    
    try:
        relatorio_partida = analisar_partida_completa(request.pgn)
        
        resumo_ia = gerar_resumo_partida(relatorio_partida["historico"])
        
        return {
            "status": "sucesso",
            "cor": request.cor_jogador,
            **relatorio_partida,
            "ai_resumo_partida": resumo_ia,
            "mensagem": "Partida inteira analisada com sucesso pelo Stockfish e resumida pelo Gemini."
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))