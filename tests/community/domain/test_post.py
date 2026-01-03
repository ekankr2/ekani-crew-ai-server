from datetime import datetime

from app.community.domain.post import Post, PostType


class TestPost:
    """Post 도메인 엔티티 테스트"""

    def test_create_topic_post(self):
        """토픽 게시글을 생성할 수 있다"""
        post = Post(
            id="post-1",
            author_id="user-1",
            title="INTJ 남자 원래 이런가요?",
            content="INTJ 남친이 답장을 안 해요...",
            post_type=PostType.TOPIC,
            topic_id="topic-1",
        )

        assert post.id == "post-1"
        assert post.author_id == "user-1"
        assert post.title == "INTJ 남자 원래 이런가요?"
        assert post.content == "INTJ 남친이 답장을 안 해요..."
        assert post.post_type == PostType.TOPIC
        assert post.topic_id == "topic-1"
        assert isinstance(post.created_at, datetime)

    def test_create_free_post(self):
        """자유 게시글을 생성할 수 있다 (topic_id 없음)"""
        post = Post(
            id="post-2",
            author_id="user-2",
            title="ENFP인데 썸남 MBTI 모르겠어요",
            content="어떻게 알 수 있을까요?",
            post_type=PostType.FREE,
        )

        assert post.id == "post-2"
        assert post.post_type == PostType.FREE
        assert post.topic_id is None
