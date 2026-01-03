from sqlalchemy import func
from sqlalchemy.orm import Session

from app.community.application.port.balance_vote_repository_port import BalanceVoteRepositoryPort
from app.community.domain.balance_game import BalanceVote, VoteChoice
from app.community.infrastructure.model.balance_vote_model import BalanceVoteModel


class MySQLBalanceVoteRepository(BalanceVoteRepositoryPort):
    """MySQL 기반 밸런스 투표 저장소"""

    def __init__(self, db_session: Session):
        self._db = db_session

    def save(self, vote: BalanceVote) -> None:
        """투표를 저장한다"""
        vote_model = BalanceVoteModel(
            id=vote.id,
            game_id=vote.game_id,
            user_id=vote.user_id,
            user_mbti=vote.user_mbti,
            choice=vote.choice.value,
            created_at=vote.created_at,
        )
        self._db.merge(vote_model)
        self._db.commit()

    def find_by_game_and_user(self, game_id: str, user_id: str) -> BalanceVote | None:
        """게임 ID와 사용자 ID로 투표를 조회한다"""
        vote_model = self._db.query(BalanceVoteModel).filter(
            BalanceVoteModel.game_id == game_id,
            BalanceVoteModel.user_id == user_id,
        ).first()

        if vote_model is None:
            return None

        return self._to_domain(vote_model)

    def find_by_game_id(self, game_id: str) -> list[BalanceVote]:
        """게임 ID로 모든 투표를 조회한다"""
        vote_models = self._db.query(BalanceVoteModel).filter(
            BalanceVoteModel.game_id == game_id
        ).all()

        return [self._to_domain(m) for m in vote_models]

    def count_by_choice(self, game_id: str, choice: VoteChoice) -> int:
        """게임 ID와 선택지로 투표 수를 계산한다"""
        return self._db.query(BalanceVoteModel).filter(
            BalanceVoteModel.game_id == game_id,
            BalanceVoteModel.choice == choice.value,
        ).count()

    def count_by_mbti_and_choice(self, game_id: str, mbti: str, choice: VoteChoice) -> int:
        """게임 ID, MBTI, 선택지로 투표 수를 계산한다"""
        return self._db.query(BalanceVoteModel).filter(
            BalanceVoteModel.game_id == game_id,
            BalanceVoteModel.user_mbti == mbti,
            BalanceVoteModel.choice == choice.value,
        ).count()

    def count_all_grouped_by_game(self) -> dict[str, dict[str, int]]:
        """모든 게임의 left/right 투표 수를 한 번에 조회한다"""
        rows = (
            self._db.query(
                BalanceVoteModel.game_id,
                BalanceVoteModel.choice,
                func.count().label("cnt"),
            )
            .group_by(BalanceVoteModel.game_id, BalanceVoteModel.choice)
            .all()
        )

        result: dict[str, dict[str, int]] = {}
        for game_id, choice, cnt in rows:
            if game_id not in result:
                result[game_id] = {"left": 0, "right": 0}
            result[game_id][choice] = cnt

        return result

    def _to_domain(self, model: BalanceVoteModel) -> BalanceVote:
        """ORM 모델을 도메인 객체로 변환한다"""
        choice = VoteChoice.LEFT if model.choice == "left" else VoteChoice.RIGHT
        return BalanceVote(
            id=model.id,
            game_id=model.game_id,
            user_id=model.user_id,
            user_mbti=model.user_mbti,
            choice=choice,
            created_at=model.created_at,
        )