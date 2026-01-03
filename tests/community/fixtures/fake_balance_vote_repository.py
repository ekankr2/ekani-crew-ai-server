from app.community.application.port.balance_vote_repository_port import BalanceVoteRepositoryPort
from app.community.domain.balance_game import BalanceVote, VoteChoice


class FakeBalanceVoteRepository(BalanceVoteRepositoryPort):
    """테스트용 Fake 밸런스 투표 저장소"""

    def __init__(self):
        self._votes: dict[str, BalanceVote] = {}

    def save(self, vote: BalanceVote) -> None:
        self._votes[vote.id] = vote

    def find_by_game_and_user(self, game_id: str, user_id: str) -> BalanceVote | None:
        for vote in self._votes.values():
            if vote.game_id == game_id and vote.user_id == user_id:
                return vote
        return None

    def find_by_game_id(self, game_id: str) -> list[BalanceVote]:
        return [v for v in self._votes.values() if v.game_id == game_id]

    def count_by_choice(self, game_id: str, choice: VoteChoice) -> int:
        return len([
            v for v in self._votes.values()
            if v.game_id == game_id and v.choice == choice
        ])

    def count_by_mbti_and_choice(self, game_id: str, mbti: str, choice: VoteChoice) -> int:
        return len([
            v for v in self._votes.values()
            if v.game_id == game_id and v.user_mbti == mbti and v.choice == choice
        ])

    def count_all_grouped_by_game(self) -> dict[str, dict[str, int]]:
        result: dict[str, dict[str, int]] = {}
        for vote in self._votes.values():
            if vote.game_id not in result:
                result[vote.game_id] = {"left": 0, "right": 0}
            result[vote.game_id][vote.choice.value] += 1
        return result
