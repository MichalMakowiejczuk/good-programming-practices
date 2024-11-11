from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionResult:
    def __init__(self, success: bool, transaction_id: Optional[str] = None, message: Optional[str] = None):
        self.success = success
        self.transaction_id = transaction_id
        self.message = message

class NetworkException(Exception):
    pass

class PaymentException(Exception):
    pass

class RefundException(Exception):
    pass

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, user_id: str, amount: float) -> TransactionResult:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> TransactionResult:
        pass

    @abstractmethod
    def get_status(self, transaction_id: str) -> TransactionStatus:
        pass
