import pytest
from datetime import datetime

from app.community.domain.balance_game import BalanceGame, BalanceVote, VoteChoice
from tests.community.fixtures.fake_balance_game_repository import FakeBalanceGameRepository


@pytest.fixture
def repository():
    """테스트용 Fake BalanceGame 저장소"""
    return FakeBalanceGameRepository()


class TestBalanceGameRepository:
    """BalanceGameRepository 테스트"""

    def test_save_and_find_game_by_id(self, repository):
        """밸런스 게임을 저장하고 id로 조회할 수 있다"""
        # Given: 유효한 밸런스 게임
        game = BalanceGame(
            id="game-123",
            question="연인이 늦잠 자서 데이트에 30분 늦음",
            option_left="솔직하게 화난다고 말한다",
            option_right="괜찮다고 하고 넘어간다",
            week_of="2025-W01",
        )

        # When: 저장하고 조회하면
        repository.save(game)
        found = repository.find_by_id("game-123")

        # Then: 저장된 게임을 찾을 수 있다
        assert found is not None
        assert found.id == "game-123"
        assert found.question == "연인이 늦잠 자서 데이트에 30분 늦음"

    def test_find_nonexistent_game_returns_none(self, repository):
        """존재하지 않는 id로 조회하면 None을 반환한다"""
        # When: 존재하지 않는 게임을 조회하면
        found = repository.find_by_id("nonexistent-game")

        # Then: None을 반환한다
        assert found is None

    def test_find_current_active(self, repository):
        """현재 활성화된 밸런스 게임을 조회할 수 있다"""
        # Given: 활성/비활성 게임
        active_game = BalanceGame(
            id="game-active",
            question="활성 게임",
            option_left="왼쪽",
            option_right="오른쪽",
            week_of="2025-W01",
            is_active=True,
        )
        inactive_game = BalanceGame(
            id="game-inactive",
            question="비활성 게임",
            option_left="왼쪽",
            option_right="오른쪽",
            week_of="2024-W52",
            is_active=False,
        )

        repository.save(active_game)
        repository.save(inactive_game)

        # When: 현재 활성 게임을 조회하면
        current = repository.find_current_active()

        # Then: 활성 게임만 반환된다
        assert current is not None
        assert current.id == "game-active"
        assert current.is_active is True

    def test_find_current_active_returns_none_when_no_active(self, repository):
        """활성 게임이 없으면 None을 반환한다"""
        # Given: 비활성 게임만 존재
        inactive_game = BalanceGame(
            id="game-inactive",
            question="비활성 게임",
            option_left="왼쪽",
            option_right="오른쪽",
            week_of="2024-W52",
            is_active=False,
        )
        repository.save(inactive_game)

        # When: 현재 활성 게임을 조회하면
        current = repository.find_current_active()

        # Then: None을 반환한다
        assert current is None
