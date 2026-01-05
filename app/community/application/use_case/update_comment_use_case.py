from app.community.application.port.comment_repository_port import CommentRepositoryPort


class UpdateCommentUseCase:
    """댓글 수정 유스케이스"""

    def __init__(self, comment_repository: CommentRepositoryPort):
        self._comment_repo = comment_repository

    def execute(self, comment_id: str, author_id: str, content: str) -> None:
        """댓글을 수정한다

        Args:
            comment_id: 댓글 ID
            author_id: 작성자 ID (권한 확인용)
            content: 수정할 내용

        Raises:
            ValueError: 댓글이 없거나 권한이 없는 경우
        """
        comment = self._comment_repo.find_by_id(comment_id)
        if comment is None:
            raise ValueError("댓글을 찾을 수 없습니다")

        if comment.author_id != author_id:
            raise ValueError("댓글을 수정할 권한이 없습니다")

        comment.content = content
        self._comment_repo.update(comment)