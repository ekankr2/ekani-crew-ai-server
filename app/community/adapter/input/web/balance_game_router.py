from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.community.application.port.balance_game_repository_port import BalanceGameRepositoryPort
from app.community.application.port.balance_vote_repository_port import BalanceVoteRepositoryPort
from app.community.application.use_case.vote_balance_game_use_case import VoteBalanceGameUseCase
from app.community.application.use_case.get_balance_result_use_case import GetBalanceResultUseCase
from app.community.domain.balance_game import VoteChoice
from app.community.infrastructure.repository.mysql_balance_game_repository import MySQLBalanceGameRepository
from app.community.infrastructure.repository.mysql_balance_vote_repository import MySQLBalanceVoteRepository
from config.database import get_db


balance_game_router = APIRouter()


def get_balance_game_repository(db: Session = Depends(get_db)) -> BalanceGameRepositoryPort:
    return MySQLBalanceGameRepository(db)


def get_balance_vote_repository(db: Session = Depends(get_db)) -> BalanceVoteRepositoryPort:
    return MySQLBalanceVoteRepository(db)


class BalanceGameResponse(BaseModel):
    id: str
    question: str
    option_left: str
    option_right: str
    week_of: str
    is_active: bool


class VoteRequest(BaseModel):
    user_id: str
    user_mbti: str
    choice: str  # "left" or "right"


class VoteResponse(BaseModel):
    vote_id: str
    choice: str


class MBTIBreakdownResponse(BaseModel):
    left: int
    right: int


class BalanceResultResponse(BaseModel):
    total_votes: int
    left_votes: int
    right_votes: int
    left_percentage: float
    right_percentage: float
    mbti_breakdown: dict[str, MBTIBreakdownResponse]


@balance_game_router.get("/balance/current")
def get_current_balance_game(
    game_repo: BalanceGameRepositoryPort = Depends(get_balance_game_repository),
) -> BalanceGameResponse:
    """현재 활성 밸런스 게임 조회"""
    game = game_repo.find_current_active()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="현재 활성화된 밸런스 게임이 없습니다",
        )

    return BalanceGameResponse(
        id=game.id,
        question=game.question,
        option_left=game.option_left,
        option_right=game.option_right,
        week_of=game.week_of,
        is_active=game.is_active,
    )


@balance_game_router.post("/balance/{game_id}/vote", status_code=status.HTTP_201_CREATED)
def vote_balance_game(
    game_id: str,
    request: VoteRequest,
    game_repo: BalanceGameRepositoryPort = Depends(get_balance_game_repository),
    vote_repo: BalanceVoteRepositoryPort = Depends(get_balance_vote_repository),
) -> VoteResponse:
    """밸런스 게임 투표"""
    choice = VoteChoice.LEFT if request.choice == "left" else VoteChoice.RIGHT

    use_case = VoteBalanceGameUseCase(game_repo, vote_repo)
    try:
        vote_id = use_case.execute(
            game_id=game_id,
            user_id=request.user_id,
            user_mbti=request.user_mbti,
            choice=choice,
        )
    except ValueError as e:
        error_message = str(e)
        if "찾을 수 없습니다" in error_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )

    return VoteResponse(vote_id=vote_id, choice=request.choice)


@balance_game_router.get("/balance/{game_id}/result")
def get_balance_result(
    game_id: str,
    game_repo: BalanceGameRepositoryPort = Depends(get_balance_game_repository),
    vote_repo: BalanceVoteRepositoryPort = Depends(get_balance_vote_repository),
) -> BalanceResultResponse:
    """밸런스 게임 결과 조회 (MBTI별 투표 비율)"""
    use_case = GetBalanceResultUseCase(game_repo, vote_repo)
    try:
        result = use_case.execute(game_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    mbti_breakdown = {
        mbti: MBTIBreakdownResponse(left=data["left"], right=data["right"])
        for mbti, data in result.mbti_breakdown.items()
    }

    return BalanceResultResponse(
        total_votes=result.total_votes,
        left_votes=result.left_votes,
        right_votes=result.right_votes,
        left_percentage=result.left_percentage,
        right_percentage=result.right_percentage,
        mbti_breakdown=mbti_breakdown,
    )