import pytest
from datetime import date

from app.community.domain.topic import Topic
from tests.community.fixtures.fake_topic_repository import FakeTopicRepository


@pytest.fixture
def repository():
    """테스트용 Fake Topic 저장소"""
    return FakeTopicRepository()


def test_save_and_find_topic_by_id(repository):
    """토픽을 저장하고 id로 조회할 수 있다"""
    # Given: 유효한 토픽
    topic = Topic(
        id="topic-123",
        title="INTJ 남자 원래 이런가요?",
        description="INTJ 남자친구의 행동에 대해 토론해보세요",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 7),
    )

    # When: 토픽을 저장하고 조회하면
    repository.save(topic)
    found = repository.find_by_id("topic-123")

    # Then: 저장된 토픽을 찾을 수 있다
    assert found is not None
    assert found.id == "topic-123"
    assert found.title == "INTJ 남자 원래 이런가요?"


def test_find_nonexistent_topic_returns_none(repository):
    """존재하지 않는 id로 조회하면 None을 반환한다"""
    # When: 존재하지 않는 토픽을 조회하면
    found = repository.find_by_id("nonexistent-topic")

    # Then: None을 반환한다
    assert found is None


def test_find_current_active_topic(repository):
    """현재 활성화된 토픽을 조회할 수 있다"""
    # Given: 활성화된 토픽과 비활성화된 토픽
    active_topic = Topic(
        id="topic-active",
        title="이번 주 토픽",
        description="활성 토픽",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 7),
        is_active=True,
    )
    inactive_topic = Topic(
        id="topic-inactive",
        title="지난 주 토픽",
        description="비활성 토픽",
        start_date=date(2024, 12, 25),
        end_date=date(2024, 12, 31),
        is_active=False,
    )

    repository.save(active_topic)
    repository.save(inactive_topic)

    # When: 현재 활성 토픽을 조회하면
    current = repository.find_current_active()

    # Then: 활성 토픽만 반환된다
    assert current is not None
    assert current.id == "topic-active"
    assert current.is_active is True


def test_find_current_active_returns_none_when_no_active_topic(repository):
    """활성 토픽이 없으면 None을 반환한다"""
    # Given: 비활성 토픽만 존재
    inactive_topic = Topic(
        id="topic-inactive",
        title="지난 주 토픽",
        description="비활성 토픽",
        start_date=date(2024, 12, 25),
        end_date=date(2024, 12, 31),
        is_active=False,
    )
    repository.save(inactive_topic)

    # When: 현재 활성 토픽을 조회하면
    current = repository.find_current_active()

    # Then: None을 반환한다
    assert current is None
