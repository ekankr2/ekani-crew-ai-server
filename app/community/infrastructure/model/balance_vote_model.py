from sqlalchemy import Column, String, DateTime
from config.database import Base


class BalanceVoteModel(Base):
    """밸런스 게임 투표 ORM 모델"""

    __tablename__ = "balance_votes"

    id = Column(String(36), primary_key=True)
    game_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    user_mbti = Column(String(4), nullable=False)
    choice = Column(String(10), nullable=False)  # "left" or "right"
    created_at = Column(DateTime, nullable=False)