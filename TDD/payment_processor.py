import logging

from payment_gateway import (
    NetworkException,
    PaymentException,
    PaymentGateway,
    RefundException,
    TransactionResult,
    TransactionStatus,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaymentProcessor:
    def __init__(self, payment_gateway: PaymentGateway):
        self.payment_gateway = payment_gateway

    def process_payment(self, user_id: str, amount: float) -> TransactionResult:
        if not user_id:
            logger.error("user_id cannot be empty")
            raise ValueError("user_id cannot be empty")
        if amount <= 0:
            logger.error("amount must be positive")
            raise ValueError("amount must be positive")

        try:
            result = self.payment_gateway.charge(user_id, amount)
            if result.success:
                logger.info(
                    f"Payment successful for user: {user_id} with transaction ID: {result.transaction_id}"
                )
            else:
                logger.warning(
                    f"Payment failed for user: {user_id}. Reason: {result.message}"
                )
            return result
        except (NetworkException, PaymentException) as e:
            logger.error(f"Payment processing error for user {user_id}: {str(e)}")
            return TransactionResult(False, message="Payment failed due to an error.")

    def refund_payment(self, transaction_id: str) -> TransactionResult:
        if not transaction_id:
            logger.error("transaction_id cannot be empty")
            raise ValueError("transaction_id cannot be empty")

        try:
            result = self.payment_gateway.refund(transaction_id)
            if result.success:
                logger.info(f"Refund successful for transaction ID {transaction_id}.")
            else:
                logger.warning(
                    f"Refund failed for transaction ID {transaction_id}. Reason: {result.message}"
                )
            return result
        except (NetworkException, RefundException) as e:
            logger.error(
                f"Refund processing error for transaction ID {transaction_id}: {str(e)}"
            )
            return TransactionResult(False, message="Refund failed due to an error.")

    def get_payment_status(self, transaction_id: str) -> TransactionStatus:
        if not transaction_id:
            logger.error("transaction_id cannot be empty")
            raise ValueError("transaction_id cannot be empty")

        try:
            status = self.payment_gateway.get_status(transaction_id)
            logger.info(f"Transaction ID {transaction_id} has status {status}.")
            return status
        except NetworkException:
            logger.error(
                f"Failed to retrieve status for transaction ID {transaction_id} due to network error."
            )
            return TransactionStatus.FAILED
