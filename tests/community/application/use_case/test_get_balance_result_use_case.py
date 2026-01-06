import pytest
from datetime import datetime

from app.community.domain.balance_game import BalanceGame, BalanceVote, VoteChoice
from app.community.application.use_case.get_balance_result_use_case import GetBalanceResultUseCase
from tests.community.fixtures.fake_balance_game_repository import FakeBalanceGameRepository
from tests.community.fixtures.fake_balance_vote_repository import FakeBalanceVoteRepository


@pytest.fixture
def game_repository():
    return FakeBalanceGameRepository()


@pytest.fixture
def vote_repository():
    return FakeBalanceVoteRepository()


@pytest.fixture
def use_case(game_repository, vote_repository):
    return GetBalanceResultUseCase(game_repository, vote_repository)


@pytest.fixture
def game_with_votes(game_repository, vote_repository):
    """투표가 있는 게임을 설정"""
    game = BalanceGame(
        id="game-123",
        question="연인이 늦잠 자서 데이트에 30분 늦음",
        option_left="솔직하게 화난다고 말한다",
        option_right="괜찮다고 하고 넘어간다",
        week_of="2025-W01",
        
    )
    game_repository.save(game)

    # 투표 데이터: INTJ 3명(좌2, 우1), ENFP 2명(좌1, 우1), ISTP 1명(좌1)
    votes = [
        BalanceVote(id="v1", game_id="game-123", user_id="u1", user_mbti="INTJ", choice=VoteChoice.LEFT),
        BalanceVote(id="v2", game_id="game-123", user_id="u2", user_mbti="INTJ", choice=VoteChoice.LEFT),
        BalanceVote(id="v3", game_id="game-123", user_id="u3", user_mbti="INTJ", choice=VoteChoice.RIGHT),
        BalanceVote(id="v4", game_id="game-123", user_id="u4", user_mbti="ENFP", choice=VoteChoice.LEFT),
        BalanceVote(id="v5", game_id="game-123", user_id="u5", user_mbti="ENFP", choice=VoteChoice.RIGHT),
        BalanceVote(id="v6", game_id="game-123", user_id="u6", user_mbti="ISTP", choice=VoteChoice.LEFT),
    ]
    for vote in votes:
        vote_repository.save(vote)

    return game


class TestGetBalanceResultUseCase:
    """GetBalanceResultUseCase 테스트"""

    def test_get_total_vote_count(self, use_case, game_with_votes):
        """전체 투표 수를 조회할 수 있다"""
        # When: 결과를 조회하면
        result = use_case.execute("game-123")

        # Then: 전체 투표 수가 맞다
        assert result.total_votes == 6
        assert result.left_votes == 4  # INTJ 2 + ENFP 1 + ISTP 1
        assert result.right_votes == 2  # INTJ 1 + ENFP 1

    def test_get_vote_percentage(self, use_case, game_with_votes):
        """투표 비율을 계산할 수 있다"""
        # When: 결과를 조회하면
        result = use_case.execute("game-123")

        # Then: 비율이 맞다 (소수점 반올림)
        assert result.left_percentage == pytest.approx(66.67, rel=0.01)
        assert result.right_percentage == pytest.approx(33.33, rel=0.01)

    def test_get_mbti_breakdown(self, use_case, game_with_votes):
        """MBTI별 투표 결과를 조회할 수 있다"""
        # When: 결과를 조회하면
        result = use_case.execute("game-123")

        # Then: MBTI별 결과가 맞다
        assert "INTJ" in result.mbti_breakdown
        assert result.mbti_breakdown["INTJ"]["left"] == 2
        assert result.mbti_breakdown["INTJ"]["right"] == 1

        assert "ENFP" in result.mbti_breakdown
        assert result.mbti_breakdown["ENFP"]["left"] == 1
        assert result.mbti_breakdown["ENFP"]["right"] == 1

        assert "ISTP" in result.mbti_breakdown
        assert result.mbti_breakdown["ISTP"]["left"] == 1
        assert result.mbti_breakdown["ISTP"]["right"] == 0

    def test_get_result_for_nonexistent_game_raises_error(self, use_case):
        """존재하지 않는 게임 결과 조회 시 에러 발생"""
        # When/Then: 존재하지 않는 게임 결과를 조회하면 에러 발생
        with pytest.raises(ValueError, match="게임을 찾을 수 없습니다"):
            use_case.execute("nonexistent-game")

    def test_get_result_with_no_votes(self, use_case, game_repository):
        """투표가 없는 게임의 결과를 조회할 수 있다"""
        # Given: 투표가 없는 게임
        game = BalanceGame(
            id="game-empty",
            question="빈 게임",
            option_left="왼쪽",
            option_right="오른쪽",
            week_of="2025-W01",
            
        )
        game_repository.save(game)

        # When: 결과를 조회하면
        result = use_case.execute("game-empty")

        # Then: 0으로 반환된다
        assert result.total_votes == 0
        assert result.left_votes == 0
        assert result.right_votes == 0
        assert result.left_percentage == 0.0
        assert result.right_percentage == 0.0
        assert result.mbti_breakdown == {}
