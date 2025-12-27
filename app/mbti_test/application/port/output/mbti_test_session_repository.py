from abc import ABC, abstractmethod
import uuid

from app.mbti_test.domain.mbti_test_session import MBTITestSession

# MBTI-4용 확장 도메인 타입(새로 추가된 파일) - 새 import 추가
from app.mbti_test.domain.mbti_result import MBTIResult, MBTITestSessionExtended

class MBTITestSessionRepositoryPort(ABC):
    @abstractmethod
    def save(self, session: MBTITestSession) -> MBTITestSession:
        pass

    @abstractmethod
    def find_by_id(self, session_id: uuid.UUID) -> MBTITestSession | None:
        pass

    # =========================
    # MBTI-4 확장 메서드 (추가만)
    # =========================

    @abstractmethod
    def add_answer(self, session_id: uuid.UUID, answer: dict) -> None:
        """
        왜 필요/언제 호출?
        - 사용자가 문항에 답변할 때 세션에 answer를 누적 저장하기 위해 호출된다.
        - 저장 방식은 구현체(Adapter)에서 결정한다.
        """
        raise NotImplementedError

    @abstractmethod
    def find_extended_by_id(
        self, session_id: uuid.UUID
    ) -> MBTITestSessionExtended | None:
        """
        왜 필요?
        - MBTI-4 결과 계산 시 answers/status/result를 포함한
          확장 도메인 세션 형태로 조회하기 위해 사용된다.
        """
        raise NotImplementedError

    @abstractmethod
    def save_result_and_complete(
            self, session_id: uuid.UUID, result: MBTIResult
    ) -> None:
        """
        왜 필요?
        - MBTI-4 최종 결과 계산 후
          결과 저장 + 세션 상태 COMPLETED 갱신을 한 번에 처리하기 위해 사용된다.
        """
        raise NotImplementedError