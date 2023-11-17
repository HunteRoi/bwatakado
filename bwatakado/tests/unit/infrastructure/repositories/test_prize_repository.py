from unittest import mock
from unittest.mock import MagicMock

from bwatakado.src.infrastructure.repositories.prize_repository import PrizeRepository


class TestPrizeRepository:
    """PrizeRepository test cases."""

    @mock.patch("bwatakado.src.infrastructure.repositories.prize_repository.Session")
    @mock.patch(
        "bwatakado.src.infrastructure.repositories.prize_repository.create_engine"
    )
    def test_delete_unknown_prize(
        self, create_engine_mock: MagicMock, session_mock: MagicMock
    ) -> None:
        """Test unknown prize deletion."""

        create_engine_mock.return_value = None
        session_mock.return_value = session_mock
        session_mock.__enter__.return_value = session_mock
        repository = PrizeRepository()

        repository.delete_prize(1)

        session_mock.execute.assert_called_once()
        session_mock.commit.assert_called()
