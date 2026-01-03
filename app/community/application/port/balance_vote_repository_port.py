from abc import ABC, abstractmethod

from app.community.domain.balance_game import BalanceVote, VoteChoice


class BalanceVoteRepositoryPort(ABC):
    """밸런스 게임 투표 저장소 포트 인터페이스"""

    @abstractmethod
    def save(self, vote: BalanceVote) -> None:
        """투표를 저장한다"""
        pass

    @abstractmethod
    def find_by_game_and_user(self, game_id: str, user_id: str) -> BalanceVote | None:
        """게임 ID와 사용자 ID로 투표를 조회한다"""
        pass

    @abstractmethod
    def find_by_game_id(self, game_id: str) -> list[BalanceVote]:
        """게임 ID로 모든 투표를 조회한다"""
        pass

    @abstractmethod
    def count_by_choice(self, game_id: str, choice: VoteChoice) -> int:
        """게임 ID와 선택지로 투표 수를 계산한다"""
        pass

    @abstractmethod
    def count_by_mbti_and_choice(self, game_id: str, mbti: str, choice: VoteChoice) -> int:
        """게임 ID, MBTI, 선택지로 투표 수를 계산한다"""
        pass

    @abstractmethod
    def count_all_grouped_by_game(self) -> dict[str, dict[str, int]]:
        """모든 게임의 left/right 투표 수를 한 번에 조회한다

        Returns:
            {game_id: {"left": count, "right": count}, ...}
        """
        pass
