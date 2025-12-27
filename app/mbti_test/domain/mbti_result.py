"""
MBTI-4(최종 결과 계산/반환)를 위해 '기존 pydantic 세션 모델'을 건드리지 않고,
점진적으로 교체/확장 가능한 순수 도메인 타입을 별도 정의한다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


class SessionStatus(str, Enum):
    """
    왜 필요?
    - 세션이 아직 진행 중인지(IN_PROGRESS) 결과까지 확정됐는지(COMPLETED)를
      유스케이스/레포/어댑터가 동일한 규칙으로 판단하기 위해.
    """
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True)
class MBTIResult:
    """
    왜 필요?
    - '최종 4글자'와 '차원별 비중(퍼센트)'을 결과 객체로 고정해서 전달/저장하기 위해.
    """
    mbti: str  # e.g. "ENTJ"
    dimension_scores: Dict[str, int]  # e.g. {"E":72,"I":28,"S":40,"N":60,"T":55,"F":45,"J":61,"P":39}
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class MBTITestSessionExtended:
    """
    왜 필요?
    - 기존 MBTITestSession(pydantic)을 깨지 않고, MBTI-4에서 필요한 필드(answers/result/status)를
      도메인 관점에서 확장해 유스케이스/레포가 점진적으로 사용하도록 하기 위해.
    """
    id: str
    user_id: str
    status: SessionStatus = SessionStatus.IN_PROGRESS
    answers: List[dict] = field(default_factory=list)
    result: Optional[MBTIResult] = None

    def is_ready(self, required_answers: int = 24) -> bool:
        """답변이 required_answers개 이상이면 결과 계산이 가능하다."""
        return len(self.answers) >= required_answers
