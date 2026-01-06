import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.community.adapter.input.web.balance_game_router import (
    balance_game_router,
    get_balance_game_repository,
    get_balance_vote_repository,
)
from app.community.domain.balance_game import BalanceGame, BalanceVote, VoteChoice
from tests.community.fixtures.fake_balance_game_repository import FakeBalanceGameRepository
from tests.community.fixtures.fake_balance_vote_repository import FakeBalanceVoteRepository


@pytest.fixture
def game_repo():
    return FakeBalanceGameRepository()


@pytest.fixture
def vote_repo():
    return FakeBalanceVoteRepository()


@pytest.fixture
def app(game_repo, vote_repo):
    app = FastAPI()
    app.include_router(balance_game_router, prefix="/community")
    app.dependency_overrides[get_balance_game_repository] = lambda: game_repo
    app.dependency_overrides[get_balance_vote_repository] = lambda: vote_repo
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def active_game(game_repo):
    game = BalanceGame(
        id="game-123",
        question="연인이 늦잠 자서 데이트에 30분 늦음",
        option_left="솔직하게 화난다고 말한다",
        option_right="괜찮다고 하고 넘어간다",
        week_of="2025-W01",
        
    )
    game_repo.save(game)
    return game


class TestBalanceGameRouter:
    """BalanceGameRouter 테스트"""

    def test_get_current_balance_game(self, client, active_game):
        """현재 활성 밸런스 게임을 조회할 수 있다"""
        # When: 현재 밸런스 게임 조회 API를 호출하면
        response = client.get("/community/balance/current")

        # Then: 활성 게임이 반환된다
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "game-123"
        assert data["question"] == "연인이 늦잠 자서 데이트에 30분 늦음"
        assert data["option_left"] == "솔직하게 화난다고 말한다"
        assert data["option_right"] == "괜찮다고 하고 넘어간다"

    def test_get_current_balance_game_returns_404_when_no_active(self, client):
        """활성 게임이 없으면 404를 반환한다"""
        # When: 활성 게임이 없는 상태에서 현재 게임 조회 API를 호출하면
        response = client.get("/community/balance/current")

        # Then: 404가 반환된다
        assert response.status_code == 404

    def test_vote_left_successfully(self, client, active_game, vote_repo):
        """왼쪽 선택지에 투표할 수 있다"""
        # When: 투표 API를 호출하면
        response = client.post(
            f"/community/balance/{active_game.id}/vote",
            json={
                "user_id": "user-123",
                "user_mbti": "INTJ",
                "choice": "left",
            },
        )

        # Then: 투표가 성공한다
        assert response.status_code == 201
        data = response.json()
        assert data["vote_id"] is not None
        assert data["choice"] == "left"

    def test_vote_right_successfully(self, client, active_game, vote_repo):
        """오른쪽 선택지에 투표할 수 있다"""
        # When: 투표 API를 호출하면
        response = client.post(
            f"/community/balance/{active_game.id}/vote",
            json={
                "user_id": "user-456",
                "user_mbti": "ENFP",
                "choice": "right",
            },
        )

        # Then: 투표가 성공한다
        assert response.status_code == 201
        data = response.json()
        assert data["vote_id"] is not None
        assert data["choice"] == "right"

    def test_duplicate_vote_returns_400(self, client, active_game, vote_repo):
        """중복 투표 시 400 에러를 반환한다"""
        # Given: 이미 투표함
        client.post(
            f"/community/balance/{active_game.id}/vote",
            json={
                "user_id": "user-123",
                "user_mbti": "INTJ",
                "choice": "left",
            },
        )

        # When: 다시 투표하면
        response = client.post(
            f"/community/balance/{active_game.id}/vote",
            json={
                "user_id": "user-123",
                "user_mbti": "INTJ",
                "choice": "right",
            },
        )

        # Then: 400 에러가 반환된다
        assert response.status_code == 400
        assert "이미 투표" in response.json()["detail"]

    def test_vote_on_nonexistent_game_returns_404(self, client):
        """존재하지 않는 게임에 투표 시 404를 반환한다"""
        # When: 존재하지 않는 게임에 투표하면
        response = client.post(
            "/community/balance/nonexistent-game/vote",
            json={
                "user_id": "user-123",
                "user_mbti": "INTJ",
                "choice": "left",
            },
        )

        # Then: 404 에러가 반환된다
        assert response.status_code == 404

    def test_get_balance_result(self, client, active_game, vote_repo):
        """밸런스 게임 결과를 조회할 수 있다"""
        # Given: 투표 데이터
        votes = [
            BalanceVote(id="v1", game_id="game-123", user_id="u1", user_mbti="INTJ", choice=VoteChoice.LEFT),
            BalanceVote(id="v2", game_id="game-123", user_id="u2", user_mbti="INTJ", choice=VoteChoice.LEFT),
            BalanceVote(id="v3", game_id="game-123", user_id="u3", user_mbti="ENFP", choice=VoteChoice.RIGHT),
        ]
        for vote in votes:
            vote_repo.save(vote)

        # When: 결과 조회 API를 호출하면
        response = client.get(f"/community/balance/{active_game.id}/result")

        # Then: 결과가 반환된다
        assert response.status_code == 200
        data = response.json()
        assert data["total_votes"] == 3
        assert data["left_votes"] == 2
        assert data["right_votes"] == 1
        assert data["left_percentage"] == pytest.approx(66.67, rel=0.01)
        assert data["right_percentage"] == pytest.approx(33.33, rel=0.01)
        assert "INTJ" in data["mbti_breakdown"]
        assert "ENFP" in data["mbti_breakdown"]

    def test_get_result_for_nonexistent_game_returns_404(self, client):
        """존재하지 않는 게임 결과 조회 시 404를 반환한다"""
        # When: 존재하지 않는 게임 결과를 조회하면
        response = client.get("/community/balance/nonexistent-game/result")

        # Then: 404 에러가 반환된다
        assert response.status_code == 404
