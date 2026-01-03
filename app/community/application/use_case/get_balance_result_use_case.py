from dataclasses import dataclass

from app.community.application.port.balance_game_repository_port import BalanceGameRepositoryPort
from app.community.application.port.balance_vote_repository_port import BalanceVoteRepositoryPort
from app.community.domain.balance_game import VoteChoice


@dataclass
class BalanceGameResult:
    """밸런스 게임 결과 DTO"""
    total_votes: int
    left_votes: int
    right_votes: int
    left_percentage: float
    right_percentage: float
    mbti_breakdown: dict[str, dict[str, int]]


class GetBalanceResultUseCase:
    """밸런스 게임 결과 조회 유스케이스"""

    def __init__(
        self,
        game_repository: BalanceGameRepositoryPort,
        vote_repository: BalanceVoteRepositoryPort,
    ):
        self._game_repository = game_repository
        self._vote_repository = vote_repository

    def execute(self, game_id: str) -> BalanceGameResult:
        """밸런스 게임 결과를 조회한다"""
        # 게임 존재 여부 확인
        game = self._game_repository.find_by_id(game_id)
        if game is None:
            raise ValueError("게임을 찾을 수 없습니다")

        # 투표 데이터 조회
        votes = self._vote_repository.find_by_game_id(game_id)

        # 전체 투표 수
        total_votes = len(votes)
        left_votes = self._vote_repository.count_by_choice(game_id, VoteChoice.LEFT)
        right_votes = self._vote_repository.count_by_choice(game_id, VoteChoice.RIGHT)

        # 비율 계산
        if total_votes > 0:
            left_percentage = round((left_votes / total_votes) * 100, 2)
            right_percentage = round((right_votes / total_votes) * 100, 2)
        else:
            left_percentage = 0.0
            right_percentage = 0.0

        # MBTI별 집계
        mbti_breakdown: dict[str, dict[str, int]] = {}
        for vote in votes:
            mbti = vote.user_mbti
            if mbti not in mbti_breakdown:
                mbti_breakdown[mbti] = {"left": 0, "right": 0}

            if vote.choice == VoteChoice.LEFT:
                mbti_breakdown[mbti]["left"] += 1
            else:
                mbti_breakdown[mbti]["right"] += 1

        return BalanceGameResult(
            total_votes=total_votes,
            left_votes=left_votes,
            right_votes=right_votes,
            left_percentage=left_percentage,
            right_percentage=right_percentage,
            mbti_breakdown=mbti_breakdown,
        )