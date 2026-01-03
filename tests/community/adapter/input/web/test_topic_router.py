import pytest
from datetime import date
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.community.adapter.input.web.topic_router import (
    topic_router,
    get_topic_repository,
)
from app.community.domain.topic import Topic
from tests.community.fixtures.fake_topic_repository import FakeTopicRepository


@pytest.fixture
def topic_repo():
    return FakeTopicRepository()


@pytest.fixture
def app(topic_repo):
    app = FastAPI()
    app.include_router(topic_router, prefix="/community")
    app.dependency_overrides[get_topic_repository] = lambda: topic_repo
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_create_topic_success(client, topic_repo):
    """토픽을 생성할 수 있다"""
    # When: 토픽 생성 API를 호출하면
    response = client.post(
        "/community/topics",
        json={
            "title": "INTJ 남자 원래 이런가요?",
            "description": "INTJ 남자친구의 행동에 대해 토론해보세요",
            "start_date": "2025-01-01",
            "end_date": "2025-01-07",
        },
    )

    # Then: 토픽이 생성된다
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "INTJ 남자 원래 이런가요?"
    assert data["description"] == "INTJ 남자친구의 행동에 대해 토론해보세요"
    assert data["is_active"] is True
    assert "id" in data


def test_get_current_topic_success(client, topic_repo):
    """현재 활성 토픽을 조회할 수 있다"""
    # Given: 활성화된 토픽이 존재
    active_topic = Topic(
        id="topic-active",
        title="이번 주 토픽",
        description="활성 토픽입니다",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 7),
        is_active=True,
    )
    topic_repo.save(active_topic)

    # When: 현재 토픽 조회 API를 호출하면
    response = client.get("/community/topics/current")

    # Then: 활성 토픽이 반환된다
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "topic-active"
    assert data["title"] == "이번 주 토픽"
    assert data["is_active"] is True


def test_get_current_topic_returns_null_when_no_active_topic(client):
    """활성 토픽이 없으면 null을 반환한다"""
    # When: 활성 토픽이 없는 상태에서 현재 토픽 조회 API를 호출하면
    response = client.get("/community/topics/current")

    # Then: 200 OK와 null이 반환된다
    assert response.status_code == 200
    assert response.json() is None
