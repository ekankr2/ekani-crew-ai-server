from sqlalchemy import Column, String, Text, DateTime, Enum
from config.database import Base


class PostModel(Base):
    """게시글 ORM 모델"""

    __tablename__ = "posts"

    id = Column(String(36), primary_key=True)
    author_id = Column(String(36), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(Enum("topic", "free", name="post_type_enum"), nullable=False)
    topic_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, nullable=False)
