"""
MBTI-4 결과 계산 시 발생하는 도메인 예외.
- Router/Adapter는 이 예외를 HTTP/응답 형태로 변환한다(도메인은 기술을 모른다).
"""


class SessionNotFound(Exception):
    """세션이 존재하지 않을 때(조회 실패)."""


class SessionNotCompleted(Exception):
    """답변 수가 부족해 결과 계산이 불가능할 때(예: 24개 미만)."""
