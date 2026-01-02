from datetime import datetime, date


class Topic:
    """이주의 토픽 도메인 엔티티"""

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        start_date: date,
        end_date: date,
        is_active: bool = True,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
