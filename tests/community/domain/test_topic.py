import pytest
from datetime import datetime, date


def test_topic_creates_with_required_fields():
    """필수 필드로 Topic 객체를 생성할 수 있다"""
    # Given: 토픽 정보
    from app.community.domain.topic import Topic

    topic_id = "topic-uuid-123"
    title = "INTJ 남자 원래 이런가요?"
    description = "INTJ 남자친구의 행동에 대해 토론해보세요"
    start_date = date(2025, 1, 1)
    end_date = date(2025, 1, 7)
    created_at = datetime.now()

    # When: Topic 객체를 생성하면
    topic = Topic(
        id=topic_id,
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        created_at=created_at,
    )

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert topic.id == topic_id
    assert topic.title == title
    assert topic.description == description
    assert topic.start_date == start_date
    assert topic.end_date == end_date
    assert topic.is_active is True  # 기본값
    assert topic.created_at == created_at