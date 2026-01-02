from sqlalchemy.orm import Session

from app.community.application.port.topic_repository_port import TopicRepositoryPort
from app.community.domain.topic import Topic
from app.community.infrastructure.model.topic_model import TopicModel


class MySQLTopicRepository(TopicRepositoryPort):
    """MySQL 기반 토픽 저장소"""

    def __init__(self, db_session: Session):
        self._db = db_session

    def save(self, topic: Topic) -> None:
        """토픽을 저장한다 (insert 또는 update)"""
        topic_model = TopicModel(
            id=topic.id,
            title=topic.title,
            description=topic.description,
            start_date=topic.start_date,
            end_date=topic.end_date,
            is_active=topic.is_active,
            created_at=topic.created_at,
        )
        self._db.merge(topic_model)
        self._db.commit()

    def find_by_id(self, topic_id: str) -> Topic | None:
        """id로 토픽을 조회한다"""
        topic_model = self._db.query(TopicModel).filter(
            TopicModel.id == topic_id
        ).first()

        if topic_model is None:
            return None

        return self._to_domain(topic_model)

    def find_current_active(self) -> Topic | None:
        """현재 활성화된 토픽을 조회한다"""
        topic_model = self._db.query(TopicModel).filter(
            TopicModel.is_active == True
        ).order_by(TopicModel.created_at.desc()).first()

        if topic_model is None:
            return None

        return self._to_domain(topic_model)

    def _to_domain(self, model: TopicModel) -> Topic:
        """ORM 모델을 도메인 객체로 변환한다"""
        return Topic(
            id=model.id,
            title=model.title,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            is_active=model.is_active,
            created_at=model.created_at,
        )
