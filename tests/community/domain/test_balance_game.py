from datetime import datetime

import pytest


def test_balance_game_creates_with_required_fields():
    """필수 필드로 BalanceGame 객체를 생성할 수 있다"""
    # Given: 밸런스 게임 정보
    from app.community.domain.balance_game import BalanceGame

    game_id = "game-uuid-123"
    question = "연인이 늦잠 자서 데이트에 30분 늦음"
    option_left = "솔직하게 화난다고 말한다"
    option_right = "괜찮다고 하고 넘어간다"
    week_of = "2025-W01"
    created_at = datetime.now()

    # When: BalanceGame 객체를 생성하면
    game = BalanceGame(
        id=game_id,
        question=question,
        option_left=option_left,
        option_right=option_right,
        week_of=week_of,
        created_at=created_at,
    )

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert game.id == game_id
    assert game.question == question
    assert game.option_left == option_left
    assert game.option_right == option_right
    assert game.week_of == week_of
    assert game.created_at == created_at


class TestBalanceVote:
    """BalanceVote 도메인 테스트"""

    def test_balance_vote_creates_with_required_fields(self):
        """필수 필드로 BalanceVote 객체를 생성할 수 있다"""
        # Given: 밸런스 투표 정보
        from app.community.domain.balance_game import BalanceVote, VoteChoice

        vote_id = "vote-uuid-123"
        game_id = "game-uuid-123"
        user_id = "user-uuid-123"
        user_mbti = "INTJ"
        choice = VoteChoice.LEFT
        created_at = datetime.now()

        # When: BalanceVote 객체를 생성하면
        vote = BalanceVote(
            id=vote_id,
            game_id=game_id,
            user_id=user_id,
            user_mbti=user_mbti,
            choice=choice,
            created_at=created_at,
        )

        # Then: 정상적으로 생성되고 값을 조회할 수 있다
        assert vote.id == vote_id
        assert vote.game_id == game_id
        assert vote.user_id == user_id
        assert vote.user_mbti == user_mbti
        assert vote.choice == VoteChoice.LEFT
        assert vote.created_at == created_at

    def test_vote_choice_enum_values(self):
        """VoteChoice enum은 LEFT와 RIGHT를 가진다"""
        from app.community.domain.balance_game import VoteChoice

        assert VoteChoice.LEFT.value == "left"
        assert VoteChoice.RIGHT.value == "right"