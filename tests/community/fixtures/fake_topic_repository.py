from app.community.application.port.topic_repository_port import TopicRepositoryPort
from app.community.domain.topic import Topic


class FakeTopicRepository(TopicRepositoryPort):
    """테스트용 Fake Topic 저장소"""

    def __init__(self):
        self._topics: dict[str, Topic] = {}

    def save(self, topic: Topic) -> None:
        self._topics[topic.id] = topic

    def find_by_id(self, topic_id: str) -> Topic | None:
        return self._topics.get(topic_id)

    def find_current_active(self) -> Topic | None:
        for topic in self._topics.values():
            if topic.is_active:
                return topic
        return None
