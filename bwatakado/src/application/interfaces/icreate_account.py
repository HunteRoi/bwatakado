from abc import ABC, abstractmethod

from bwatakado.src.application.use_cases.create_account.account_data import AccountData
from bwatakado.src.domain.entities.customer import Customer


class ICreateAccount(ABC):
    """Interface for creating a customer account"""

    @abstractmethod
    def execute(self, data: AccountData) -> Customer:
        """Create a customer account"""
