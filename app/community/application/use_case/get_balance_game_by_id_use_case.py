from dataclasses import dataclass
from datetime import datetime, timedelta

from app.community.application.port.balance_game_repository_port import (
    BalanceGameRepositoryPort,
)
from app.community.application.port.balance_vote_repository_port import (
    BalanceVoteRepositoryPort,
)
from app.community.application.port.comment_repository_port import CommentRepositoryPort
from app.user.application.port.user_repository_port import UserRepositoryPort


@dataclass
class BalanceGameCommentDTO:
    """밸런스 게임 댓글 DTO"""

    id: str
    author_id: str
    author_mbti: str | None
    content: str
    created_at: datetime


@dataclass
class BalanceGameDetail:
    """밸런스 게임 상세 DTO"""

    id: str
    question: str
    option_left: str
    option_right: str
    week_of: str
    total_votes: int
    left_votes: int
    right_votes: int
    left_percentage: float
    right_percentage: float
    comments: list[BalanceGameCommentDTO]
    is_votable: bool
    created_at: datetime
    user_choice: str | None = None  # 사용자의 투표 선택 (left/right/None)


class GetBalanceGameByIdUseCase:
    """밸런스 게임 상세 조회 유스케이스"""

    VOTABLE_DAYS = 30  # 투표 가능 기간 (일)

    def __init__(
        self,
        balance_game_repository: BalanceGameRepositoryPort,
        balance_vote_repository: BalanceVoteRepositoryPort,
        comment_repository: CommentRepositoryPort,
        user_repository: UserRepositoryPort,
    ):
        self._game_repo = balance_game_repository
        self._vote_repo = balance_vote_repository
        self._comment_repo = comment_repository
        self._user_repo = user_repository

    def execute(self, game_id: str, user_id: str | None = None) -> BalanceGameDetail:
        """밸런스 게임 상세를 조회한다"""
        game = self._game_repo.find_by_id(game_id)
        if game is None:
            raise ValueError("게임을 찾을 수 없습니다")

        # 투표 집계 (한 번의 쿼리로 left/right 모두 조회)
        vote_counts = self._vote_repo.count_by_game(game_id)
        left_votes = vote_counts["left"]
        right_votes = vote_counts["right"]
        total_votes = left_votes + right_votes

        left_percentage = (left_votes / total_votes * 100) if total_votes > 0 else 0.0
        right_percentage = (right_votes / total_votes * 100) if total_votes > 0 else 0.0

        # 사용자 투표 조회
        user_choice: str | None = None
        if user_id:
            user_vote = self._vote_repo.find_by_game_and_user(game_id, user_id)
            if user_vote:
                user_choice = user_vote.choice.value

        # 댓글 조회
        comments = self._comment_repo.find_by_target("balance_game", game_id)

        # 댓글 작성자 MBTI 일괄 조회 (N+1 방지)
        author_ids = list(set(c.author_id for c in comments))
        users = self._user_repo.find_by_ids(author_ids)
        user_mbti_map = {u.id: u.mbti.value if u.mbti else None for u in users}

        comment_dtos = [
            BalanceGameCommentDTO(
                id=comment.id,
                author_id=comment.author_id,
                author_mbti=user_mbti_map.get(comment.author_id),
                content=comment.content,
                created_at=comment.created_at,
            )
            for comment in comments
        ]

        is_votable = self._is_votable(game.created_at)

        return BalanceGameDetail(
            id=game.id,
            question=game.question,
            option_left=game.option_left,
            option_right=game.option_right,
            week_of=game.week_of,
            total_votes=total_votes,
            left_votes=left_votes,
            right_votes=right_votes,
            left_percentage=left_percentage,
            right_percentage=right_percentage,
            comments=comment_dtos,
            is_votable=is_votable,
            created_at=game.created_at,
            user_choice=user_choice,
        )

    def _is_votable(self, created_at: datetime) -> bool:
        """투표 가능 여부를 판단한다 (생성 후 30일 이내)"""
        cutoff = datetime.now() - timedelta(days=self.VOTABLE_DAYS)
        return created_at > cutoff
