import pytest
from datetime import datetime

from app.community.domain.balance_game import BalanceVote, VoteChoice
from tests.community.fixtures.fake_balance_vote_repository import FakeBalanceVoteRepository


@pytest.fixture
def repository():
    """테스트용 Fake BalanceVote 저장소"""
    return FakeBalanceVoteRepository()


class TestBalanceVoteRepository:
    """BalanceVoteRepository 테스트"""

    def test_save_vote(self, repository):
        """투표를 저장할 수 있다"""
        # Given: 투표 정보
        vote = BalanceVote(
            id="vote-123",
            game_id="game-123",
            user_id="user-123",
            user_mbti="INTJ",
            choice=VoteChoice.LEFT,
        )

        # When: 저장하면
        repository.save(vote)

        # Then: 저장된 투표를 찾을 수 있다
        found = repository.find_by_game_and_user("game-123", "user-123")
        assert found is not None
        assert found.id == "vote-123"

    def test_find_by_game_and_user_returns_none_when_not_found(self, repository):
        """존재하지 않는 투표 조회 시 None 반환"""
        # When: 존재하지 않는 투표를 조회하면
        found = repository.find_by_game_and_user("game-123", "user-123")

        # Then: None을 반환한다
        assert found is None

    def test_find_by_game_id(self, repository):
        """게임 ID로 모든 투표를 조회할 수 있다"""
        # Given: 여러 투표
        vote1 = BalanceVote(
            id="vote-1",
            game_id="game-123",
            user_id="user-1",
            user_mbti="INTJ",
            choice=VoteChoice.LEFT,
        )
        vote2 = BalanceVote(
            id="vote-2",
            game_id="game-123",
            user_id="user-2",
            user_mbti="ENFP",
            choice=VoteChoice.RIGHT,
        )
        vote3 = BalanceVote(
            id="vote-3",
            game_id="game-456",
            user_id="user-3",
            user_mbti="ISTP",
            choice=VoteChoice.LEFT,
        )

        repository.save(vote1)
        repository.save(vote2)
        repository.save(vote3)

        # When: 게임 ID로 조회하면
        votes = repository.find_by_game_id("game-123")

        # Then: 해당 게임의 투표만 반환된다
        assert len(votes) == 2
        assert all(v.game_id == "game-123" for v in votes)

    def test_count_by_choice(self, repository):
        """선택지별 투표 수를 계산할 수 있다"""
        # Given: 여러 투표
        votes = [
            BalanceVote(id="v1", game_id="game-123", user_id="u1", user_mbti="INTJ", choice=VoteChoice.LEFT),
            BalanceVote(id="v2", game_id="game-123", user_id="u2", user_mbti="ENFP", choice=VoteChoice.LEFT),
            BalanceVote(id="v3", game_id="game-123", user_id="u3", user_mbti="ISTP", choice=VoteChoice.RIGHT),
        ]
        for vote in votes:
            repository.save(vote)

        # When: 선택지별 개수를 조회하면
        left_count = repository.count_by_choice("game-123", VoteChoice.LEFT)
        right_count = repository.count_by_choice("game-123", VoteChoice.RIGHT)

        # Then: 올바른 개수를 반환한다
        assert left_count == 2
        assert right_count == 1

    def test_count_by_mbti_and_choice(self, repository):
        """MBTI별, 선택지별 투표 수를 계산할 수 있다"""
        # Given: 여러 투표
        votes = [
            BalanceVote(id="v1", game_id="game-123", user_id="u1", user_mbti="INTJ", choice=VoteChoice.LEFT),
            BalanceVote(id="v2", game_id="game-123", user_id="u2", user_mbti="INTJ", choice=VoteChoice.LEFT),
            BalanceVote(id="v3", game_id="game-123", user_id="u3", user_mbti="INTJ", choice=VoteChoice.RIGHT),
            BalanceVote(id="v4", game_id="game-123", user_id="u4", user_mbti="ENFP", choice=VoteChoice.LEFT),
            BalanceVote(id="v5", game_id="game-123", user_id="u5", user_mbti="ENFP", choice=VoteChoice.RIGHT),
        ]
        for vote in votes:
            repository.save(vote)

        # When: MBTI별 선택지 개수를 조회하면
        intj_left = repository.count_by_mbti_and_choice("game-123", "INTJ", VoteChoice.LEFT)
        intj_right = repository.count_by_mbti_and_choice("game-123", "INTJ", VoteChoice.RIGHT)
        enfp_left = repository.count_by_mbti_and_choice("game-123", "ENFP", VoteChoice.LEFT)
        enfp_right = repository.count_by_mbti_and_choice("game-123", "ENFP", VoteChoice.RIGHT)

        # Then: 올바른 개수를 반환한다
        assert intj_left == 2
        assert intj_right == 1
        assert enfp_left == 1
        assert enfp_right == 1
