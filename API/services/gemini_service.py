import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi encontrada! Verifique o seu arquivo .env.")

genai.configure(api_key=API_KEY)

def gerar_explicacao_jogada(fen: str, melhor_lance: str, avaliacao: int) -> str:
    """
    Usa o Gemini para traduzir a avaliação técnica do Stockfish em uma explicação didática em português do Brasil.
    """
    prompt = f"""
    Você está atuando como um treinador de xadrez especialista, didático e amigável.
    Analise os seguintes dados técnicos fornecidos pelo motor Stockfish para uma determinada posição de xadrez:
    
    - Posição atual (FEN): {fen}
    - Melhor lance recomendado: {melhor_lance}
    - Avaliação da posição (em centipawns): {avaliacao}

    Com base nisso, crie uma explicação clara, curta e motivadora (em português do Brasil) direcionada a um jogador que quer entender o porquê de este lance ser o mais forte nesta posição específica.
    """

    try:
        model = genai.GenerativeModel('gemini-3.5-flash-lite')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Não foi possível gerar a explicação no momento: {str(e)}"


def gerar_resumo_partida(historico_lances: list) -> str:
    """
    Usa o Gemini para gerar um resumo analítico e motivador da partida inteira.
    """
    total_lances = len(historico_lances)
    
    prompt = f"""
    Você está atuando como um treinador de xadrez especialista. 
    Uma partida de xadrez acaba de ser jogada, contendo {total_lances} jogadas no total.
    O histórico de avaliações e lances foi processado pelo motor Stockfish.
    
    Com base nisso, elabore um resumo analítico, construtivo e motivador (em português do Brasil) avaliando o ritmo geral da partida, o desempenho estratégico e dicas de melhoria para o jogador.
    """

    try:
        model = genai.GenerativeModel('gemini-3.5-flash-lite')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Não foi possível gerar o resumo da partida no momento: {str(e)}"