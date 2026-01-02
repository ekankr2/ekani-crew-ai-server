from sqlalchemy import Column, String, Text, Date, Boolean, DateTime
from config.database import Base


class TopicModel(Base):
    """이주의 토픽 ORM 모델"""

    __tablename__ = "topics"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
