from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):
    """
    왜 필요?
    - MBTI-4에서 결과 확정 후 User.mbti를 업데이트해야 하는데,
      UseCase가 DB/ORM을 몰라야 하므로 인터페이스로 분리한다.
    """

    @abstractmethod
    def update_mbti(self, user_id: uuid.UUID, mbti: str) -> None:
        """MBTI-4 결과 확정 직후 사용자 프로필(User)에 mbti를 반영할 때 호출된다."""
        raise NotImplementedError
