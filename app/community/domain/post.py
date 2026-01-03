from datetime import datetime
from enum import Enum


class PostType(Enum):
    """게시글 유형"""
    TOPIC = "topic"  # 이주의 토픽 관련 글
    FREE = "free"    # 자유 게시글


class Post:
    """토론 게시글 도메인 엔티티"""

    def __init__(
        self,
        id: str,
        author_id: str,
        title: str,
        content: str,
        post_type: PostType,
        topic_id: str | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.author_id = author_id
        self.title = title
        self.content = content
        self.post_type = post_type
        self.topic_id = topic_id
        self.created_at = created_at or datetime.now()
