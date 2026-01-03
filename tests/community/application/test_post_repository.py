import pytest

from app.community.domain.post import Post, PostType
from tests.community.fixtures.fake_post_repository import FakePostRepository


class TestPostRepository:
    """PostRepository 테스트"""

    @pytest.fixture
    def repository(self):
        return FakePostRepository()

    @pytest.fixture
    def topic_post(self):
        return Post(
            id="post-1",
            author_id="user-1",
            title="INTJ 남자 원래 이런가요?",
            content="INTJ 남친이 답장을 안 해요...",
            post_type=PostType.TOPIC,
            topic_id="topic-1",
        )

    @pytest.fixture
    def free_post(self):
        return Post(
            id="post-2",
            author_id="user-2",
            title="ENFP인데 썸남 MBTI 모르겠어요",
            content="어떻게 알 수 있을까요?",
            post_type=PostType.FREE,
        )

    def test_save_post(self, repository, topic_post):
        """게시글을 저장할 수 있다"""
        repository.save(topic_post)

        saved = repository.find_by_id("post-1")
        assert saved is not None
        assert saved.title == "INTJ 남자 원래 이런가요?"

    def test_find_by_id_returns_none_when_not_found(self, repository):
        """존재하지 않는 게시글 조회 시 None을 반환한다"""
        result = repository.find_by_id("non-existent")
        assert result is None

    def test_find_all_returns_posts_ordered_by_created_at_desc(
        self, repository, topic_post, free_post
    ):
        """모든 게시글을 최신순으로 조회한다"""
        repository.save(topic_post)
        repository.save(free_post)

        posts = repository.find_all()

        assert len(posts) == 2
        # 더 최근에 저장된 free_post가 먼저 나와야 함
        assert posts[0].id == "post-2"
        assert posts[1].id == "post-1"

    def test_find_by_post_type(self, repository, topic_post, free_post):
        """게시글 유형별로 조회할 수 있다"""
        repository.save(topic_post)
        repository.save(free_post)

        topic_posts = repository.find_by_post_type(PostType.TOPIC)
        free_posts = repository.find_by_post_type(PostType.FREE)

        assert len(topic_posts) == 1
        assert topic_posts[0].id == "post-1"
        assert len(free_posts) == 1
        assert free_posts[0].id == "post-2"
