from datetime import datetime
from enum import Enum


class VoteChoice(Enum):
    """투표 선택지"""
    LEFT = "left"
    RIGHT = "right"


class BalanceGame:
    """밸런스 게임 도메인 엔티티"""

    def __init__(
        self,
        id: str,
        question: str,
        option_left: str,
        option_right: str,
        week_of: str,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.question = question
        self.option_left = option_left
        self.option_right = option_right
        self.week_of = week_of
        self.created_at = created_at or datetime.now()


class BalanceVote:
    """밸런스 게임 투표 도메인 엔티티"""

    def __init__(
        self,
        id: str,
        game_id: str,
        user_id: str,
        user_mbti: str,
        choice: VoteChoice,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.game_id = game_id
        self.user_id = user_id
        self.user_mbti = user_mbti
        self.choice = choice
        self.created_at = created_at or datetime.now()