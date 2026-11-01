from pydantic import BaseModel, Field

class GameAnalysisRequest(BaseModel):
    pgn: str = Field(..., description="The PGN string of the chess game to analyze")
    cor_jogador: str = Field(default="white", description="The color of the player to analyze (white or black)")