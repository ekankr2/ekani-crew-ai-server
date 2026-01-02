from abc import ABC, abstractmethod

from app.community.domain.topic import Topic


class TopicRepositoryPort(ABC):
    """토픽 저장소 포트 인터페이스"""

    @abstractmethod
    def save(self, topic: Topic) -> None:
        """토픽을 저장한다"""
        pass

    @abstractmethod
    def find_by_id(self, topic_id: str) -> Topic | None:
        """id로 토픽을 조회한다"""
        pass

    @abstractmethod
    def find_current_active(self) -> Topic | None:
        """현재 활성화된 토픽을 조회한다"""
        pass
