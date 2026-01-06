from sqlalchemy import Column, String, Text, DateTime
from config.database import Base


class BalanceGameModel(Base):
    """밸런스 게임 ORM 모델"""

    __tablename__ = "balance_games"

    id = Column(String(36), primary_key=True)
    question = Column(Text, nullable=False)
    option_left = Column(String(255), nullable=False)
    option_right = Column(String(255), nullable=False)
    week_of = Column(String(10), nullable=False)  # e.g., "2025-W01"
    created_at = Column(DateTime, nullable=False)